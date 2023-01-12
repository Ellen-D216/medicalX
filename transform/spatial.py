import SimpleITK as sitk
import numpy as np
from typing import Sequence, Tuple, Union, overload

from data.image import Image, Subject
from .utils import Transform, ResampleUtils, TransformFactory
from config import TransformType, InterpolatorType, ImageType, PadType, KernelType


class Pad(Transform):
    def __init__(self, mode:PadType, low:Tuple[int, int], up:Tuple[int, int],
                 pad_value=0, decay:float=1., transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        if mode == PadType.PadConstant:
            pad_filter = sitk.ConstantPadImageFilter()
            pad_filter.SetConstant(pad_value)
        elif mode == PadType.PadMirror:
            pad_filter = sitk.MirrorPadImageFilter()
            pad_filter.SetDecayBase(decay)
        elif mode == PadType.PadWrap:
            pad_filter = sitk.WrapPadImageFilter()
        pad_filter.SetPadLowerBound(low)
        pad_filter.SetPadUpperBound(up)
        self.total_filter.append(pad_filter)

def pad(image:Union[sitk.Image, Image, Subject], mode:PadType, low:Tuple[int, int], up:Tuple[int, int],
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


class Resample(Transform):
    @overload
    def __init__(self, transform:sitk.Transform, interpolator:InterpolatorType, 
                 cast=None, transform_keys:Tuple[str]=None):
        super().__init__(transform_keys)
        resample_filter = self._get_base_resample_filter(transform, interpolator, cast)
        self.total_filter.append(resample_filter)

    @overload
    def __init__(self, transform:sitk.Transform, interpolator:InterpolatorType, reference:Union[Image, sitk.Image], 
                 cast=None, transform_keys:Tuple[str]=None):
        super().__init__(transform_keys)
        resample_filter = self._get_base_resample_filter(transform, interpolator, cast)
        resample_filter.SetReferenceImage(reference)
        self.total_filter.append(resample_filter)

    @overload
    def __init__(self, transform:sitk.Transform, interpolator:InterpolatorType, 
                 out_size:Sequence[int], out_spacing:Sequence[float], out_origin:Sequence[float], out_direction:Sequence[float],
                 cast=None, transform_keys:Tuple[str]=None):
        super().__init__(transform_keys)
        resample_filter = self._get_base_resample_filter(transform, interpolator, cast)
        resample_filter.SetSize(out_size)
        resample_filter.SetOutputOrigin(out_origin)
        resample_filter.SetOutputSpacing(out_spacing)
        resample_filter.SetOutputDirection(out_direction)
        self.total_filter.append(resample_filter)

    def _get_base_resample_filter(self, transform, interpolator, cast):
        resample_filter = sitk.ResampleImageFilter()
        resample_filter.SetTransform(transform)
        resample_filter.SetInterpolator(interpolator)
        if cast is not None:
            resample_filter.SetOutputPixelType(cast)
        return resample_filter


class Resize(Transform):
    def __init__(self, target_size:Sequence[int], transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        self.target_size = target_size

    def __call__(self, image: Union[sitk.Image, Image, Subject]):
        target_spacing = ResampleUtils.get_target_spacing(image, self.target_size)
        interpolator = InterpolatorType.Linear if image.type == ImageType.Scalar else InterpolatorType.NearestNeighbor
        
        resample_filter = sitk.ResampleImageFilter()
        resample_filter.SetTransform(TransformFactory.register(TransformType.Identity))
        resample_filter.SetInterpolator(interpolator)
        resample_filter.SetSize(self.target_size)
        resample_filter.SetOutputSpacing(target_spacing)
        resample_filter.SetOutputOrigin(image.GetOrigin())
        resample_filter.SetOutputDirection(image.GetDirection())
        self.total_filter.append(resample_filter)
        return super().__call__(image)


class BinaryMorphologicalOpen(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball,
                 background:float = 0, foreground:float = 1,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        open_filter = sitk.BinaryMorphologicalOpeningImageFilter()
        open_filter.SetBackgroundValue(background)
        open_filter.SetForegroundValue(foreground)
        open_filter.SetKernelType(kernel)
        open_filter.SetKernelRadius(radius)
        self.total_filter.append(open_filter)


class BinaryMorphologicalClose(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball,
                 foreground:float = 1, transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        close_filter = sitk.BinaryMorphologicalClosingImageFilter()
        close_filter.SetForegroundValue(foreground)
        close_filter.SetKernelType(kernel)
        close_filter.SetKernelRadius(radius)
        self.total_filter.append(close_filter)


class GrayscaleMorphologicalOpen(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball, safe_border:bool = True,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        open_filter = sitk.GrayscaleMorphologicalOpeningImageFilter()
        open_filter.SetKernelRadius(radius)
        open_filter.SetKernelType(kernel)
        open_filter.SetSafeBorder(safe_border)
        self.total_filter.append(open_filter)


class GrayScaleMorphologicalClose(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball, safe_border:bool = True,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        close_filter = sitk.GrayscaleMorphologicalClosingImageFilter()
        close_filter.SetKernelRadius(radius)
        close_filter.SetKernelType(kernel)
        close_filter.SetSafeBorder(safe_border)
        self.total_filter.append(close_filter)


class BinaryMorphologicalErode(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball,
                 background:float = 0, foreground:float = 1, boundary_to_foreground:bool = True,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        erode_filter = sitk.BinaryErodeImageFilter()
        erode_filter.SetBackgroundValue(background)
        erode_filter.SetForegroundValue(foreground)
        erode_filter.SetKernelRadius(radius)
        erode_filter.SetKernelType(kernel)
        erode_filter.SetBoundaryToForeground(boundary_to_foreground)
        self.total_filter.append(erode_filter)


class BinaryMorphologicalDilate(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball,
                 background:float = 0, foreground:float = 1, boundary_to_foreground:bool = True,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        dilate_filter = sitk.BinaryDilateImageFilter()
        dilate_filter.SetBackgroundValue(background)
        dilate_filter.SetForegroundValue(foreground)
        dilate_filter.SetKernelRadius(radius)
        dilate_filter.SetKernelType(kernel)
        dilate_filter.SetBoundaryToForeground(boundary_to_foreground)
        self.total_filter.append(dilate_filter)


class GrayscaleMorphologicalErode(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        erode_filter = sitk.GrayscaleErodeImageFilter()
        erode_filter.SetKernelRadius(radius)
        erode_filter.SetKernelType(kernel)
        self.total_filter.append(erode_filter)


class GrayscaleMorphologicalDilate(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], kernel=KernelType.Ball,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        dilate_filter = sitk.GrayscaleDilateImageFilter()
        dilate_filter.SetKernelRadius(radius)
        dilate_filter.SetKernelType(kernel)
        self.total_filter.append(dilate_filter)


class ObjectMorphologicalErode(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], object_value:float, kernel=KernelType.Ball,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        erode_filter = sitk.ErodeObjectMorphologyImageFilter()
        erode_filter.SetObjectValue(object_value)
        erode_filter.SetKernelRadius(radius)
        erode_filter.SetKernelType(kernel)
        self.total_filter.append(erode_filter)


class ObjectMorphologicalDilate(Transform):
    def __init__(self, radius:Union[int, Sequence[int]], object_value:float, kernel=KernelType.Ball,
                 transform_keys: Tuple[str] = None) -> None:
        super().__init__(transform_keys)
        dilate_filter = sitk.DilateObjectMorphologyImageFilter()
        dilate_filter.SetObjectValue(object_value)
        dilate_filter.SetKernelRadius(radius)
        dilate_filter.SetKernelType(kernel)
        self.total_filter.append(dilate_filter)