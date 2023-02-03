import numpy as np
import SimpleITK as sitk
from typing import Sequence, Dict

from .painter import get_colormap


def convert_label_to_labelmap(labels:Dict[str, np.ndarray], cmap:str="jet"):
    category = len(labels) + 1
    colormap = get_colormap(cmap, category)
    colortable = dict(); colortable["background"] = (0, colormap(0)[:3])
    for i, label_name in enumerate(labels.keys()):
        if i == 0: labelmap = np.zeros_like(labels[label_name])
        labelmap[labels[label_name] > 0] = i + 1
        colortable[label_name] = (i+1, colormap(i+1)[:3])
    labelmap = colormap(labelmap)[..., :3]
    return labelmap, colortable

def blend(image:np.ndarray, labels:Dict[str, np.ndarray], cmap:str="jet", alpha:float=0.5):
    shape = image.shape
    image = image.astype(np.float64)
    image = image - image.min(); image = image / image.max()
    if (len(shape) == 2) or (len(shape) == 3 and not shape[-1] in (3, 4)):
        image = np.concatenate([image[..., np.newaxis]]*3, axis=-1)
    labelmap, colortable = convert_label_to_labelmap(labels, cmap)
    blend_image = image.copy()
    for i in range(image.shape[-1]):
        for label in labels.values():
            blend_image[..., i][label > 0] = image[..., i][label > 0] * (1-alpha) + labelmap[..., i][label > 0] * alpha
    return (blend_image * 255).astype(np.uint8), colortable
