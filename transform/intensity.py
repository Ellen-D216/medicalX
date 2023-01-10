import SimpleITK as sitk
import numpy as np
from typing import Tuple, Union

from data.image import Image, Subject
from .transform import Transform, CompositeImageFilter
from config import Scalar, Label


clip = sitk.Clamp
class Clip(Transform):
    def __init__(self, low:float=-1000, up:float=1000, cast=None, transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        clip_filter = sitk.ClampImageFilter()
        clip_filter.SetLowerBound(low)
        clip_filter.SetUpperBound(up)
        if cast is not None:
            clip_filter.SetOutputPixelType(cast)
        self.total_filter.append(clip_filter)


rescale = sitk.RescaleIntensity
class Rescale(Transform):
    def __init__(self, out_min=0, out_max=255, 
                 percentiles: Tuple[float, float] = (0, 100), cast=None, transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        self.percentiles = percentiles
        rescale_filter = sitk.RescaleIntensityImageFilter()
        rescale_filter.SetOutputMaximum(out_max)
        rescale_filter.SetOutputMinimum(out_min)
        self.total_filter.append(rescale_filter)

        if cast is not None:
            cast_filter = sitk.CastImageFilter()
            cast_filter.SetOutputPixelType(cast)
            self.total_filter.append(cast_filter)

    def __call__(self, image: Union[sitk.Image, Image, Subject]):
        if isinstance(image, (Image, sitk.Image)):
            image = self._rescale(image)
            return super().__call__(image)
        elif isinstance(image, Subject):
            subj = self._subject_apply(image)
            return super().__call__(subj)

    def _rescale(self, image: Union[Image, sitk.Image]):
        array = sitk.GetArrayFromImage(image)
        cutoff = np.percentile(array.ravel(), self.percentiles)
        np.clip(array, *cutoff, out=array)
        return sitk.GetImageFromArray(array).CopyInformation(image)



normalize = sitk.Normalize
class Normalize(Transform):
    def __init__(self, transform_keys:Tuple[str]=None) -> None:
        super().__init__(transform_keys)
        self.total_filter.append(sitk.NormalizeImageFilter())