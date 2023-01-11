import SimpleITK as sitk
import numpy as np
from typing import Any, Callable, List, Sequence, Union, Tuple

from data.image import Image, Subject


class Composite:
    def __init__(self, composite:List[Any]) -> None:
        self.composite = composite

    def append(self, plugin):
        self.composite.append(plugin)

    def pop(self, index):
        self.composite.pop(index)

    def clear(self):
        self.composite.clear()

    def __len__(self):
        return len(self.composite)

    def __getitem__(self, index):
        return self.composite[index]


class CompositeImageFilter(Composite):
    def __call__(self, image:Union[sitk.Image, Image]):
        for filter in self.composite:
            image = filter.Execute(image)
        return Image(image)


class CompositeTransform(Composite):
    def __call__(self, image:Union[sitk.Image, Image, Subject]):
        for transform in self.composite:
            image = transform(image)
        return Image(image) if isinstance(image, sitk.Image) else image


class Transform:
    def __init__(self, transform_keys:Tuple[str]=None) -> None:
        self.total_filter = CompositeImageFilter([])
        self.keys = transform_keys

    def __call__(self, image:Union[sitk.Image, Image, Subject]):
        if len(self.total_filter):
            if isinstance(image, (Image, sitk.Image)):
                return self.total_filter(image)
            elif isinstance(image, Subject):
                return self._subject_apply(image)
        else:
            raise ValueError("You don't give filters!")
 
    def _subject_apply(self, subj:Subject, apply:Callable=None):
            subj_ = subj.clone()
            keys = tuple(subj.keys()) if self.keys is None else self.keys
            call = self.total_filter if apply is None else apply
            for name, value in subj_.images.items():
                if name in keys:
                    subj_[name] = call(value)
            return subj_


class ResampleUtils:
    @staticmethod
    def get_grid_size(image:Union[Image, sitk.Image], transform:sitk.Transform):
        transformed_extreme_points = ResampleUtils.get_transformed_extreme_points(image, transform)
        min_x = min(transformed_extreme_points)[0]
        min_y = min(transformed_extreme_points, key=lambda p: p[1])[1]
        max_x = max(transformed_extreme_points)[0]
        max_y = max(transformed_extreme_points, key=lambda p: p[1])[1]
        if image.GetDimension() == 2:
            return {
                'size': [
                    int((max_x - min_x) / image.GetSpacing()[0]),
                    int((max_y - min_y) / image.GetSpacing()[1])
                ],
                'origin': np.asarray([min_x, min_y])
            }
        elif image.GetDimension() == 3:
            min_z = min(transformed_extreme_points, key=lambda p: p[2])[2]
            max_z = max(transformed_extreme_points, key=lambda p: p[2])[2]
            return {
                'size': [
                    int((max_x - min_x) / image.GetSpacing()[0]),
                    int((max_y - min_y) / image.GetSpacing()[1]),
                    int((max_z - min_z) / image.GetSpacing()[2])
                ],
                'origin': np.asarray([min_x, min_y, min_z])
            }

    @staticmethod
    def get_extreme_points(image:Union[Image, sitk.Image]):
        if image.GetDimension() == 2:
            return [
                image.TransformIndexToPhysicalPoint((0, 0)),
                image.TransformIndexToPhysicalPoint((image.GetWidth(), 0)),
                image.TransformIndexToPhysicalPoint((image.GetWidth(), image.GetHeight())),
                image.TransformIndexToPhysicalPoint((0, image.GetHeight())),
            ]
        elif image.GetDimension() == 3:
            return [
                image.TransformIndexToPhysicalPoint((0, 0, 0)),
                image.TransformIndexToPhysicalPoint((image.GetWidth(), 0, 0)),
                image.TransformIndexToPhysicalPoint((image.GetWidth(), image.GetHeight(), 0)),
                image.TransformIndexToPhysicalPoint((image.GetWidth(), image.GetHeight(), image.GetDepth())),
                image.TransformIndexToPhysicalPoint((0, image.GetHeight(), 0)),
                image.TransformIndexToPhysicalPoint((0, image.GetHeight(), image.GetDepth())),
                image.TransformIndexToPhysicalPoint((image.GetWidth(), 0, image.GetDepth())),
                image.TransformIndexToPhysicalPoint((0, 0, image.GetDepth())),
            ]

    @staticmethod
    def get_transformed_extreme_points(image:Union[Image, sitk.Image], transform:sitk.Transform):
        extreme_points = ResampleUtils.get_extreme_points(image)
        inverse_transform:sitk.Transform = transform.GetInverse()
        return [inverse_transform.TransformPoint(p) for p in extreme_points]

    @staticmethod
    def get_target_size(image:Union[Image, sitk.Image], target_spacing:Sequence[float]):
        return np.asarray([
            image.GetSize()[i] * image.GetSpacing()[i] / target_spacing[i] for i in range(image.GetDimension())
        ])
        
    @staticmethod
    def get_target_spacing(image:Union[Image, sitk.Image], target_size:Sequence[float]):
        return np.asarray([
            image.GetSize()[i] * image.GetSpacing()[i] / target_size[i] for i in range(image.GetDimension())
        ])