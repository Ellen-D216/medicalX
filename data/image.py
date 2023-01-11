import os
from typing import List, Sequence, Union
import SimpleITK as sitk
import numpy as np
from torch import from_numpy

from . import io
from config import Scalar, Label

class Image(sitk.Image):
    def __init__(
        self,
        image: Union[str, List[str], sitk.Image],
        orientation: str = 'LPS',
        type: str = Scalar
    ) -> None:
        try:
            if isinstance(image, sitk.Image): super().__init__(image)
            else: super().__init__(io.imread(image, orientation))
        except:
            raise ValueError("Input must be a SimpleITK Image, a file path or a list of file paths!")
        
        self.type = type
        self.channels = self.GetNumberOfComponentsPerPixel()

    @property
    def array(self):
        return sitk.GetArrayFromImage(self)

    @property
    def dim(self):
        return self.GetDimension()
    
    @property
    def spacing(self):
        return np.asarray(self.GetSpacing())
    
    @spacing.setter
    def spacing(self, spacing:Sequence[float]):
        self.SetSpacing(spacing)

    @property
    def origin(self):
        return np.asarray(self.GetOrigin())

    @origin.setter
    def origin(self, origin:Sequence[float]):
        self.SetOrigin(origin)

    @property
    def direction(self):
        return np.asarray(self.GetDirection())

    @direction.setter
    def direction(self, direction:Sequence[float]):
        self.SetDirection(direction)

    @property
    def info(self):
        return {
            'spacing': self.spacing,
            'origin': self.origin,
            'direction': self.direction
        }

    @info.setter
    def info(self, info:dict):
        self.spacing = info['spacing']
        self.origin = info['origin']
        self.direction = info['direction']

    @property
    def center(self):
        return np.asarray(
            self.TransformContinuousIndexToPhysicalPoint(self.size / 2.)
        )

    @property
    def shape(self):
        return self.array.shape

    @property
    def size(self):
        return np.asarray(self.GetSize())

    @property
    def tensor(self):
        if self.channels == 1:
            return from_numpy(self.array[np.newaxis, ...]) # put channel first
        elif self.channels in (3, 4):
            return from_numpy(np.moveaxis(self.array, -1, 0))

    def save(self, path:Union[str, List[str]]):
        io.imsave(self, path)


class Subject(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images = self.get_images()

    def get_images(self):
        images = {}
        for name, image in self.items():
            if isinstance(image, (Image, sitk.Image)):
                images[name] = image
        return images
    
    def clone(self):
        from copy import deepcopy
        return deepcopy(self)