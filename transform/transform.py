import SimpleITK as sitk
from typing import List, Union, Tuple

from data.image import Image, Subject
from config import Translation, Scale, Similarity, Euler, Affine


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


class TransformFactory:
    @staticmethod
    def register(transform_type:str, dim:int, *args):
        if transform_type == Translation:
            return TransformFactory.get_translation_transform(dim, *args)
        elif transform_type == Scale:
            return TransformFactory.get_translation_transform(dim, *args)
        elif transform_type == Similarity:
            return TransformFactory.get_similarity_transform(dim, *args)
        elif transform_type == Euler:
            return TransformFactory.get_euler_transform(dim, *args)
        elif transform_type == Affine:
            return TransformFactory.get_affine_transform(*args)

    @staticmethod
    def get_translation_transform(dim, *args):
        '''
        args: VectorDouble offset
        '''
        return sitk.TranslationTransform(dim, *args)

    @staticmethod
    def get_scale_transform(dim, *args):
        '''
        args: VectorDouble scale
        '''
        return sitk.ScaleTransform(dim, *args)

    @staticmethod
    def get_similarity_transform(dim, *args):
        '''
        args: double scaleFactor, double angle, VectorDouble translation, VectorDouble fixedCenter
        '''
        if dim == 2:
            return sitk.Similarity2DTransform(*args)
        elif dim == 3:
            return sitk.Similarity3DTransform(*args)

    @staticmethod
    def get_euler_transform(dim, *args):
        '''
        args: VectorDouble fixedCenter, double angle, VectorDouble translation
        '''
        if dim == 2:
            return sitk.Euler2DTransform(*args)
        elif dim == 3:
            return sitk.Euler3DTransform(*args)

    @staticmethod
    def get_affine_transform(*args):
        '''
        args: VectorDouble matrix, VectorDouble translation, VectorDouble fixedCenter
        '''
        return sitk.AffineTransform(*args)