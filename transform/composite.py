import SimpleITK as sitk
from typing import List, Union
from data.image import Image

class CompositeImageFilter:
    def __init__(self, filters:List[sitk.ImageFilter]) -> None:
        self.composite = filters

    def append(self, filter:sitk.ImageFilter):
        self.composite.append(filter)

    def pop(self, index):
        self.composite.pop(index)

    def clear(self):
        self.composite = []

    def __len__(self):
        return len(self.composite)

    def __getitem__(self, index):
        return self.composite[index]

    def __call__(self, image:Union[sitk.Image, Image]):
        for filter in self.composite:
            image = filter.Execute(image)
        return Image(image)

