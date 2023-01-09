import SimpleITK as sitk
import numpy as np
from typing import Sequence, Tuple, Union

from data.image import Image, Subject
from .transform import Transform
from config import *


constant_pad = sitk.ConstantPad
mirror_pad = sitk.MirrorPad
wrap_pad = sitk.WrapPad
class Pad(Transform):
    def __init__(self, mode:str, low:Tuple[int, int], up:Tuple[int, int],
                 pad_value=0, decay:float=1.) -> None:
        super().__init__()
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


crop = sitk.Crop
class Crop(Transform):
    def __init__(self, low:Tuple[int, int], up:Tuple[int, int]) -> None:
        super().__init__()
        crop_filter = sitk.CropImageFilter()
        crop_filter.SetLowerBoundaryCropSize(low)
        crop_filter.SetUpperBoundaryCropSize(up)
        self.total_filter.append(crop_filter)


flip = sitk.Flip
class Flip(Transform):
    def __init__(self, axes:Sequence[bool]) -> None:
        super().__init__()
        flip_filter = sitk.FlipImageFilter()
        flip_filter.SetFlipAxes(axes)
        self.total_filter.append(flip_filter)