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
    def __init__(self) -> None:
        self.total_filter = CompositeImageFilter([])

    def __call__(self, image:Union[sitk.Image, Image, Subject], transform_keys:Tuple[str]=None):
        if len(self.total_filter):
            if isinstance(image, (Image, sitk.Image)):
                return self.total_filter(image)
            elif isinstance(image, Subject):
                subj = image.clone()
                keys = tuple(subj.keys()) if transform_keys is None else transform_keys
                for name, value in image.images.items():
                    if name in keys:
                        subj[name] = self.total_filter(value)
                return subj
        else:
            raise ValueError("You don't give filters!")


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

    def __call__(self, image:Union[sitk.Image, Image, Subject], transform_keys:Tuple[str]=None):
        for transform in self.composite:
            image = transform(image, transform_keys)
        return Image(image) if isinstance(image, sitk.Image) else image