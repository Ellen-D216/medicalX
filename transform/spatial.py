import SimpleITK as sitk
import numpy as np
from typing import Sequence, Tuple, Union

from data.image import Image, Subject
from .utils import Transform
from config import *


class Pad(Transform):
    def __init__(self, mode:str, low:Tuple[int, int], up:Tuple[int, int],
                 pad_value=0, decay:float=1., transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        if mode == PadConstant:
            pad_filter = sitk.ConstantPadImageFilter()
            pad_filter.SetConstant(pad_value)
        elif mode == PadMirror:
            pad_filter = sitk.MirrorPadImageFilter()
            pad_filter.SetDecayBase(decay)
        elif mode == PadWrap:
            pad_filter = sitk.WrapPadImageFilter()
        pad_filter.SetPadLowerBound(low)
        pad_filter.SetPadUpperBound(up)
        self.total_filter.append(pad_filter)
def pad(image:Union[sitk.Image, Image, Subject], mode:str, low:Tuple[int, int], up:Tuple[int, int],
        pad_value=0, decay:float=1., transform_keys:Tuple[str]=None):
    return Pad(mode, low, up, pad_value, decay, transform_keys)(image)


class Crop(Transform):
    def __init__(self, low:Tuple[int, int], up:Tuple[int, int], transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        crop_filter = sitk.CropImageFilter()
        crop_filter.SetLowerBoundaryCropSize(low)
        crop_filter.SetUpperBoundaryCropSize(up)
        self.total_filter.append(crop_filter)
def crop(image:Union[sitk.Image, Image, Subject], low:Tuple[int, int], 
         up:Tuple[int, int], transform_keys:Tuple[str]=None):
    return Crop(low, up, transform_keys)(image)


class Flip(Transform):
    def __init__(self, axes:Sequence[bool], transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        flip_filter = sitk.FlipImageFilter()
        flip_filter.SetFlipAxes(axes)
        self.total_filter.append(flip_filter)
def flip(image:Union[sitk.Image, Image, Subject], axes:Sequence[bool], transform_keys:Tuple[str]=None):
    return Flip(axes, transform_keys)(image)


# resample = sitk.Resample
class Resample(Transform):
    def __init__(
        self, 
        transform_keys:Tuple[str]=None
    ) -> None:
        super().__init__(transform_keys)