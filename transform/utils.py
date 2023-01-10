import SimpleITK as sitk
from typing import List, Union, Tuple

from data.image import Image, Subject


class CompositeImageFilter:
    def __init__(self, filters:List[sitk.ImageFilter]) -> None:
        self.composite = filters

    def append(self, filter:sitk.ImageFilter):
        self.composite.append(filter)

    def pop(self, index):
        self.composite.pop(index)

    def clear(self):
        self.composite.clear()

    def __len__(self):
        return len(self.composite)

    def __getitem__(self, index):
        return self.composite[index]

    def __call__(self, image:Union[sitk.Image, Image]):
        for filter in self.composite:
            image = filter.Execute(image)
        return Image(image)


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

    def _subject_apply(self, subj:Subject):
            subj_ = subj.clone()
            keys = tuple(subj.keys()) if self.keys is None else self.keys
            for name, value in subj_.images.items():
                if name in keys:
                    subj_[name] = self.total_filter(value)
            return subj_



class CompositeTransform:
    def __init__(self, transform:List[Transform]) -> None:
        self.composite = transform

    def append(self, transform:Transform):
        self.composite.append(transform)

    def pop(self, index):
        self.composite.pop(index)

    def clear(self):
        self.composite.clear()

    def __len__(self):
        return len(self.composite)

    def __getitem__(self, index):
        return self.composite[index]

    def __call__(self, image:Union[sitk.Image, Image, Subject]):
        for transform in self.composite:
            image = transform(image)
        return Image(image) if isinstance(image, sitk.Image) else image
