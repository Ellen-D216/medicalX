import SimpleITK as sitk
import numpy as np
from typing import Tuple, Union

from data.image import Image, Subject
from .composite import CompositeImageFilter
from config import Scalar, Label

class IntensityTransform:
    def __init__(self) -> None:
        self.total_filter = CompositeImageFilter([])

    def __call__(self, image:Union[sitk.Image, Image, Subject]):
        if len(self.total_filter):
            if isinstance(image, (Image, sitk.Image)):
                return self.total_filter(image)
            elif isinstance(image, Subject):
                subj = image.clone()
                for name, value in image.images.items():
                    if value.type == Scalar:
                        subj[name] = self.total_filter(value)
                return subj
        else:
            raise ValueError("You don't give filters!")


clip = sitk.Clamp
class Clip(IntensityTransform):
    def __init__(self, low:float=-1000, up:float=1000, cast=None) -> None:
        super().__init__()
        clip_filter = sitk.ClampImageFilter()
        clip_filter.SetLowerBound(low)
        clip_filter.SetUpperBound(up)
        if cast is not None:
            clip_filter.SetOutputPixelType(cast)
        self.total_filter.append(clip_filter)


rescale = sitk.RescaleIntensity
class Rescale(IntensityTransform):
    def __init__(self, out_min=0, out_max=255, 
                 percentiles: Tuple[float, float] = (0, 100), cast=None) -> None:
        super().__init__()
        self.percentiles = percentiles
        rescale_filter = sitk.RescaleIntensityImageFilter()
        rescale_filter.SetOutputMaximum(out_max)
        rescale_filter.SetOutputMinimum(out_min)
        self.total_filter.append(rescale_filter)

        if cast is not None:
            cast_filter = sitk.CastImageFilter()
            cast_filter.SetOutputPixelType(cast)
            self.total_filter.append(cast_filter)

    def __call__(self, image: Union[sitk.Image, Image, Subject]) -> Image:
        if isinstance(image, (Image, sitk.Image)):
            image = self._rescale(image)
            return super().__call__(image)
        elif isinstance(image, Subject):
            subj = image.clone()
            for name, value in image.images.items():
                if value.type == Scalar:
                    subj[name] = self._rescale(value)
            return super().__call__(subj)

    def _rescale(self, image: Union[Image, sitk.Image]):
        array = sitk.GetArrayFromImage(image)
        cutoff = np.percentile(array.ravel(), self.percentiles)
        np.clip(array, *cutoff, out=array)
        return sitk.GetImageFromArray(array).CopyInformation(image)



normalize = sitk.Normalize
class Normalize(IntensityTransform):
    def __init__(self) -> None:
        super().__init__()
        self.total_filter.append(sitk.NormalizeImageFilter())