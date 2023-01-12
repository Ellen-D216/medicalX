import SimpleITK as sitk
from enum import Enum

##########################
###      Image Type     ###
##########################
class ImageType(Enum):
    Scalar = 'scalar'
    Label = 'label'

##########################
###      Pad Type     ###
##########################
class PadType(Enum):
    PadConstant = 'constant'
    PadMirror = 'mirror'
    PadWrap = 'wrap'

##########################
###      Data Type     ###
##########################
class DataType:
    Uint8 = sitk.sitkUInt8

    Int8 = sitk.sitkInt8

    UInt16 = sitk.sitkUInt16

    Int16 = sitk.sitkInt16

    UInt32 = sitk.sitkUInt32

    Int32 = sitk.sitkInt32

    UInt64 = sitk.sitkUInt64

    Int64 = sitk.sitkInt64

    Float32 = sitk.sitkFloat32

    Float64 = sitk.sitkFloat64

    ComplexFloat32 = sitk.sitkComplexFloat32

    ComplexFloat64 = sitk.sitkComplexFloat64

    VectorUInt8 = sitk.sitkVectorUInt8

    VectorInt8 = sitk.sitkVectorInt8

    VectorUInt16 = sitk.sitkVectorUInt16

    VectorInt16 = sitk.sitkVectorInt16

    VectorUInt32 = sitk.sitkVectorUInt32

    VectorInt32 = sitk.sitkVectorInt32

    VectorUInt64 = sitk.sitkVectorUInt64

    VectorInt64 = sitk.sitkVectorInt64

    VectorFloat32 = sitk.sitkVectorFloat32

    VectorFloat64 = sitk.sitkVectorFloat64

    LabelUInt8 = sitk.sitkLabelUInt8

    LabelUInt16 = sitk.sitkLabelUInt16

    LabelUInt32 = sitk.sitkLabelUInt32

    LabelUInt64 = sitk.sitkLabelUInt64

##########################
###   Interpolator Type     
##########################

class InterpolatorType:
    NearestNeighbor = sitk.sitkNearestNeighbor

    Linear = sitk.sitkLinear

    BSpline = sitk.sitkBSpline

    BSpline1 = sitk.sitkBSpline1

    BSpline2 = sitk.sitkBSpline2

    BSpline3 = sitk.sitkBSpline3

    BSpline4 = sitk.sitkBSpline4

    BSpline5 = sitk.sitkBSpline5

    Gaussian = sitk.sitkGaussian

    LabelGaussian = sitk.sitkLabelGaussian

    HammingWindowedSinc = sitk.sitkHammingWindowedSinc

    CosineWindowedSinc = sitk.sitkCosineWindowedSinc

    WelchWindowedSinc = sitk.sitkWelchWindowedSinc

    LanczosWindowedSinc = sitk.sitkLanczosWindowedSinc

    BlackmanWindowedSinc = sitk.sitkBlackmanWindowedSinc

    BSplineResampler = sitk.sitkBSplineResampler

    BSplineResamplerOrder3 = sitk.sitkBSplineResamplerOrder3

    BSplineResamplerOrder1 = sitk.sitkBSplineResamplerOrder1

    BSplineResamplerOrder2 = sitk.sitkBSplineResamplerOrder2

    BSplineResamplerOrder4 = sitk.sitkBSplineResamplerOrder4

    BSplineResamplerOrder5 = sitk.sitkBSplineResamplerOrder5

##########################
###   kernel Type     
##########################

class KernelType:
    Annulus = sitk.sitkAnnulus

    Ball = sitk.sitkBall

    Box = sitk.sitkBox

    Cross = sitk.sitkCross

    Polygon3 = sitk.sitkPolygon3

    Polygon4 = sitk.sitkPolygon4

    Polygon5 = sitk.sitkPolygon5

    Polygon6 = sitk.sitkPolygon6

    Polygon7 = sitk.sitkPolygon7

    Polygon8 = sitk.sitkPolygon8

    Polygon9 = sitk.sitkPolygon9

##########################
###   transform Type     
##########################

class TransformType:
    Identity = sitk.sitkIdentity

    Translation = sitk.sitkTranslation

    Scale = sitk.sitkScale

    ScaleLogarithmic = sitk.sitkScaleLogarithmic

    Euler = sitk.sitkEuler

    Similarity = sitk.sitkSimilarity

    QuaternionRigid = sitk.sitkQuaternionRigid

    Versor = sitk.sitkVersor

    VersorRigid = sitk.sitkVersorRigid

    ScaleSkewVersor = sitk.sitkScaleSkewVersor

    ComposeScaleSkewVersor = sitk.sitkComposeScaleSkewVersor

    ScaleVersor = sitk.sitkScaleVersor

    Affine = sitk.sitkAffine

    Composite = sitk.sitkComposite

    DisplacementField = sitk.sitkDisplacementField

    BSplineTransform = sitk.sitkBSplineTransform