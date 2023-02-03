import SimpleITK as sitk
import numpy as np
from vtkmodules.all import (
    vtkImageData, vtkImageViewer2,
    vtkRenderWindow, vtkRenderWindowInteractor,
    vtkInteractorStyleUser, vtkCommand
)
from typing import Union

from utils.convert import numpy_to_vtk

OrientationXY = 2
OrientationYZ = 0
OrientationXZ = 1

class Viewer:
    def __init__(self) -> None:
        self._init = 0
        self.move = False
        self.shape = None
        self.orientation = OrientationXY
        self.image_data:vtkImageData = None
        self.viewer = vtkImageViewer2()
        
        self.style = vtkInteractorStyleUser()
        self.style.AddObserver(vtkCommand.KeyPressEvent, self.on_key_press)
        self.style.AddObserver(vtkCommand.MouseWheelForwardEvent, self.on_mousewheel_forward)
        self.style.AddObserver(vtkCommand.MouseWheelBackwardEvent, self.on_mousewheel_backward)
        self.style.AddObserver(vtkCommand.LeftButtonPressEvent, self.on_left_mousebutton_press)
        self.style.AddObserver(vtkCommand.LeftButtonReleaseEvent, self.on_left_mousebutton_release)
        self.style.AddObserver(vtkCommand.MouseMoveEvent, self.on_mouse_move)
        
        self.interactor = vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.viewer.GetRenderWindow())
        self.interactor.RemoveAllObservers()
        self.interactor.SetInteractorStyle(self.style)

    def set_image_data(self, image:Union[sitk.Image, vtkImageData]):
        if isinstance(image, sitk.Image):
            self.image_data = numpy_to_vtk(
                np.flip(sitk.GetArrayFromImage(image), 1),
                np.asarray(image.GetSpacing()),
                np.asarray(image.GetOrigin()),
                np.asarray(image.GetDirection())
            )
        elif isinstance(image, vtkImageData):
            self.image_data = image
        self.shape = self.image_data.GetDimensions()

    def initialize(self, wl:float=0, ww:float=2000):
        self.viewer.SetColorLevel(wl); self.viewer.SetColorWindow(ww)
        self.viewer.SetInputData(self.image_data)
        self.viewer.SetSliceOrientation(self.orientation)
        self.viewer.SetSlice(self.shape[self.orientation]//2)
        self.render()
        self.interactor.Initialize()
        self.interactor.Start()
        self._init = 1

    def render(self):
        self.viewer.Render()

    def on_key_press(self, vtk_object, vtk_event):
        key = self.interactor.GetKeyCode()
        if key == 'x' or key == 'X':
            self.viewer.SetSliceOrientationToYZ()
            self.viewer.SetSlice(self.shape[0]//2)
            self.orientation = OrientationYZ
        elif key == 'y' or key == 'Y':
            self.viewer.SetSliceOrientationToXZ()
            self.viewer.SetSlice(self.shape[1]//2)
            self.orientation = OrientationXZ
        elif key == 'z' or key == 'Z':
            self.viewer.SetSliceOrientationToXY()
            self.viewer.SetSlice(self.shape[2]//2)
            self.orientation = OrientationXY
        elif key == 'r' or key == 'R':
            self.viewer.SetColorLevel(0)
            self.viewer.SetColorWindow(2000)
        self.render()

    def on_left_mousebutton_press(self, vtk_object, vtk_event):
        self.move = True

    def on_left_mousebutton_release(self, vtk_object, vtk_event):
        self.move = False

    def on_mouse_move(self, vtk_object, vtk_event):
        if self.move:
            first = self.interactor.GetEventPosition()
            second = self.interactor.GetLastEventPosition()
            if abs(first[1] - second[1]) > 0:
                self.viewer.SetColorWindow(self.viewer.GetColorWindow() + (second[1] - first[1])*10)
            if abs(first[0] - second[0]) > 0:
                self.viewer.SetColorLevel(self.viewer.GetColorLevel() + (second[0] - first[0])*10)
            self.render()

    def on_mousewheel_forward(self, vtk_object, vtk_event):
        slice = self.viewer.GetSlice()
        if self.interactor.GetControlKey():
            self.viewer.GetRenderer().GetActiveCamera().Zoom(0.9)
        elif slice > 0:
            self.viewer.SetSlice(slice - 1)
        self.render()
        
    def on_mousewheel_backward(self, vtk_object, vtk_event):
        slice = self.viewer.GetSlice()
        if self.interactor.GetControlKey():
            self.viewer.GetRenderer().GetActiveCamera().Zoom(1.1)
        elif self.orientation == OrientationXY:
            if slice < self.shape[2] - 1:
                self.viewer.SetSlice(slice + 1)
        elif self.orientation == OrientationYZ:
            if slice < self.shape[0] - 1:
                self.viewer.SetSlice(slice + 1)
        elif self.orientation == OrientationXZ:
            if slice < self.shape[1] - 1:
                self.viewer.SetSlice(slice + 1)
        self.render()