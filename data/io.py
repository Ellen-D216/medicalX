import os
from typing import Union, List
import SimpleITK as sitk
import numpy as np

formats = ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']
image_2d_formats = formats + [s.upper() for s in formats]


def imread(image_path:Union[str, List[str]], orientation:str='LPS') -> sitk.Image:
    try:
        if isinstance(image_path, str) and os.path.isdir(image_path):
            image = sitk.ReadImage(sitk.ImageSeriesReader_GetGDCMSeriesFileNames(image_path))
        else:
            image = sitk.ReadImage(image_path)
        if orientation == 'LPS':
            return image
        else:
            return sitk.DICOMOrient(image, orientation)
    except Exception as e:
        print(e)

def imsave(image:sitk.Image, image_path:Union[str, List[str]]):
    example = image_path if isinstance(image_path, str) else image_path[0]
    if example.endswith(image_2d_formats):
        image = sitk.Cast(
            sitk.RescaleIntensity(image), sitk.sitkUInt8
        )
    sitk.WriteImage(image, image_path)