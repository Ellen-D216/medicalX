from typing import Sequence, overload
import numpy as np
import SimpleITK as sitk

class TranslationTransform(sitk.TranslationTransform):
    @overload
    def __init__(self, dim:int, offset:Sequence[float]=None):
        offset = [0]*dim if offset is None else offset
        super().__init__(dim, offset)

    @overload
    def __init__(self, transform:sitk.TranslationTransform):
        super().__init__(transform)

    @property
    def offset(self):
        return self.GetOffset()

    @offset.setter
    def offset(self, value:Sequence[float]):
        self.SetOffset(value)


class ScaleTransform(sitk.ScaleTransform):
    @overload
    def __init__(self, dim:int, scale:Sequence[float]=None):
        scale = [1]*dim if scale is None else scale
        super().__init__(dim, scale)

    @overload
    def __init__(self, transform:sitk.ScaleTransform):
        super().__init__(transform)

    @property
    def scale(self):
        return self.GetScale()

    @scale.setter
    def scale(self, value:Sequence[float]):
        self.SetScale(value)

    @property
    def center(self):
        return self.GetCenter()

    @center.setter
    def center(self, value:Sequence[float]):
        self.SetCenter(value)

    @property
    def matrix(self):
        return self.GetMatrix()


class Similarity2DTransform(sitk.Similarity2DTransform):
    @overload
    def __init__(self):
        super().__init__()

    @overload
    def __init__(self, scale:float, angle:float=0., translation:Sequence[float]=[0., 0.], center:Sequence[float]=[0., 0.]):
        super().__init__(scale, angle, translation, center)

    @overload
    def __init__(self, transform:sitk.Similarity2DTransform):
        super().__init__(transform)

    @property
    def scale(self):
        return self.GetScale()

    @scale.setter
    def scale(self, value:Sequence[float]):
        self.SetScale(value)

    @property
    def center(self):
        return self.GetCenter()

    @center.setter
    def center(self, value:Sequence[float]):
        self.SetCenter(value)

    @property
    def angle(self):
        return self.GetAngle()

    @angle.setter
    def angle(self, value:float):
        self.SetAngle(value)

    @property
    def translation(self):
        return self.GetTranslation()

    @translation.setter
    def translation(self, value:Sequence[float]):
        self.SetTranslation(value)

    @property
    def matrix(self):
        return self.GetMatrix()

    @matrix.setter
    def matrix(self, value:Sequence[float]):
        self.SetMatrix(value)


class Similarity3DTransform(sitk.Similarity3DTransform):
    @overload
    def __init__(self):
        super().__init__()

    @overload
    def __init__(self, versor:Sequence[float], scale:float=1., translation:Sequence[float]=[0., 0., 0.], center:Sequence[float]=[0., 0., 0.]):
        super().__init__(scale, versor, translation, center)

    @overload
    def __init__(self, axis:Sequence[int], scale:float=1., angle:float=0., translation:Sequence[float]=[0., 0., 0.], center:Sequence[float]=[0., 0., 0.]):
        theta = np.deg2rad(angle)
        vector = axis * np.sin(theta/2)
        versor = [*vector, np.cos(theta/2)]
        super().__init__(scale, versor, translation, center)

    @overload
    def __init__(self, transform:sitk.Similarity3DTransform):
        super().__init__(transform)

    @property
    def scale(self):
        return self.GetScale()

    @scale.setter
    def scale(self, value:Sequence[float]):
        self.SetScale(value)

    @property
    def center(self):
        return self.GetCenter()

    @center.setter
    def center(self, value:Sequence[float]):
        self.SetCenter(value)

    @property
    def rotation(self):
        return self.GetVersor()

    @rotation.setter
    def rotation(self, value:Sequence[float]):
        self.SetRotation(value)

    @property
    def translation(self):
        return self.GetTranslation()

    @translation.setter
    def translation(self, value:Sequence[float]):
        self.SetTranslation(value)

    @property
    def matrix(self):
        return self.GetMatrix()

    @matrix.setter
    def matrix(self, value:Sequence[float]):
        self.SetMatrix(value)


class Euler2DTransform(sitk.Euler2DTransform):
    @overload
    def __init__(self):
        super().__init__()

    @overload
    def __init__(self, center:Sequence[float]=[0., 0.], angle:float=0., translation:Sequence[float]=[0., 0.]):
        super().__init__(center, angle, translation)

    @overload
    def __init__(self, transform:sitk.Euler2DTransform):
        super().__init__(transform)

    @property
    def center(self):
        return self.GetCenter()

    @center.setter
    def center(self, value:Sequence[float]):
        self.SetCenter(value)

    @property
    def angle(self):
        return self.GetAngle()

    @angle.setter
    def angle(self, value:float):
        self.SetAngle(value)

    @property
    def translation(self):
        return self.GetTranslation()

    @translation.setter
    def translation(self, value:Sequence[float]):
        self.SetTranslation(value)

    @property
    def matrix(self):
        return self.GetMatrix()

    @matrix.setter
    def matrix(self, value:Sequence[float]):
        self.SetMatrix(value)


class Euler3DTransform(sitk.Euler3DTransform):
    @overload
    def __init__(self):
        super().__init__()

    @overload
    def __init__(self, center:Sequence[float]=[0., 0., 0.], angleX:float=0., angleY:float=0., angleZ:float=0.,
                 translation:Sequence[float]=[0., 0., 0.]):
        super().__init__(center, angleX, angleY, angleZ, translation)

    @overload
    def __init__(self, transform:sitk.Euler3DTransform):
        super().__init__(transform)

    @property
    def center(self):
        return self.GetCenter()

    @center.setter
    def center(self, value:Sequence[float]):
        self.SetCenter(value)

    @property
    def rotation(self):
        return (self.GetAngleX(), self.GetAngleY(), self.GetAngleZ())

    @rotation.setter
    def rotation(self, value:Sequence[float]):
        self.SetRotation(*value)

    @property
    def translation(self):
        return self.GetTranslation()

    @translation.setter
    def translation(self, value:Sequence[float]):
        self.SetTranslation(value)

    @property
    def matrix(self):
        return self.GetMatrix()

    @matrix.setter
    def matrix(self, value:Sequence[float]):
        self.SetMatrix(value)


class AffineTransform(sitk.AffineTransform):
    @overload
    def __init__(self, dim:int):
        super().__init__(dim)

    @overload
    def __init__(self, transform:sitk.AffineTransform):
        super().__init__(transform)

    @overload
    def __init__(self, matrix:Sequence[float], translation:Sequence[float], center:Sequence[float]):
        super().__init__(matrix, translation, center)

    @property
    def translation(self):
        return self.GetTranslation()

    @translation.setter
    def translation(self, value:Sequence[float]):
        self.SetTranslation(value)

    @property
    def matrix(self):
        return self.GetMatrix()

    @matrix.setter
    def matrix(self, value:Sequence[float]):
        self.SetMatrix(value)

    @property
    def center(self):
        return self.GetCenter()

    @center.setter
    def center(self, value:Sequence[float]):
        self.SetCenter(value)