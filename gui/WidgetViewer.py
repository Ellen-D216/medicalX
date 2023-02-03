import numpy as np
import SimpleITK as sitk
from vtkmodules.all import (
    vtkImageData, vtkImageViewer2,
    vtkRenderWindow, vtkRenderWindowInteractor,
    vtkInteractorStyleUser, vtkCommand,
    VTK_SHORT, VTK_UNSIGNED_CHAR
)

from utils.convert import numpy_to_vtk
from typing import List

OrientationXY = 2
OrientationYZ = 0
OrientationXZ = 1

class WidgetViewer:
    def __init__(self, qinteractor) -> None:
        self.move = False
        self.orientation = OrientationXY
        self.image:vtkImageData = None
        self.viewer = vtkImageViewer2()
        self.overlay_image:vtkImageData = None

        self.style = vtkInteractorStyleUser()
        self.style.AddObserver(vtkCommand.KeyPressEvent, self.on_key_press)
        self.style.AddObserver(vtkCommand.MouseWheelForwardEvent, self.on_mousewheel_forward)
        self.style.AddObserver(vtkCommand.MouseWheelBackwardEvent, self.on_mousewheel_backward)
        self.style.AddObserver(vtkCommand.LeftButtonPressEvent, self.on_left_mousebutton_press)
        self.style.AddObserver(vtkCommand.LeftButtonReleaseEvent, self.on_left_mousebutton_release)
        self.style.AddObserver(vtkCommand.MouseMoveEvent, self.on_mouse_move)
        
        self.interactor = qinteractor
        self.viewer.SetRenderWindow(qinteractor.GetRenderWindow())
        self.interactor.RemoveAllObservers()
        self.interactor.SetInteractorStyle(self.style)

    def set_image_data(self, image:sitk.Image):
        if isinstance(image, sitk.Image):
            self.image = self._get_image_data(image)
        elif isinstance(image, vtkImageData):
            self.image = image
        self.viewer.SetInputData(self.image)
        self.shape = self.image.GetDimensions()

    def _get_image_data(self, image:sitk.Image, dtype=VTK_SHORT):
        return numpy_to_vtk(
            np.flip(sitk.GetArrayFromImage(image), 1),
            np.asarray(image.GetSpacing()),
            np.asarray(image.GetOrigin()),
            np.asarray(image.GetDirection()),
            dtype
        )

    def viewer_initialize(self):
        self.viewer.SetColorLevel(0); self.viewer.SetColorWindow(2000)
        self.viewer.SetSliceOrientation(self.orientation)
        self.viewer.SetSlice(self.shape[self.orientation]//2)
        self.viewer.Render()
        self.interactor.Initialize()
        self.interactor.Start()

    def set_slice(self, slice:int):
        self.viewer.SetSlice(slice)
        self.viewer.Render()

    def label_overlay(self, overlay_image:sitk.Image):
        self.overlay_image = self._get_image_data(overlay_image, VTK_UNSIGNED_CHAR)
        self.viewer.SetInputData(self.overlay_image)
        self.viewer.Render()

    def get_wlww(self):
        return self.viewer.GetColorLevel(), self.viewer.GetColorWindow()

    def set_wlww(self, wl:float, ww:float):
        self.viewer.SetColorLevel(wl)
        self.viewer.SetColorWindow(ww)
        self.viewer.Render()

    def reset(self):
        self.set_image_data(self.image)
        self.overlay_image = None
        self.viewer.Render()

    def on_key_press(self, vtk_object, vtk_event):
        key = self.interactor.GetKeyCode()
        if key == 'r' or key == 'R':
            if self.overlay_image is None:
                self.viewer.SetColorLevel(0)
                self.viewer.SetColorWindow(2000)
            else:
                self.viewer.SetColorLevel(127.5)
                self.viewer.SetColorWindow(255.0)
        self.viewer.Render()

    def on_left_mousebutton_press(self, vtk_object, vtk_event):
        self.move = True

    def on_left_mousebutton_release(self, vtk_object, vtk_event):
        self.move = False

    def on_mouse_move(self, vtk_object, vtk_event):
        if self.move:
            if self.overlay_image is None:
                first = self.interactor.GetEventPosition()
                second = self.interactor.GetLastEventPosition()
                if abs(first[1] - second[1]) > 0:
                    self.viewer.SetColorWindow(self.viewer.GetColorWindow() + (second[1] - first[1])*10)
                if abs(first[0] - second[0]) > 0:
                    self.viewer.SetColorLevel(self.viewer.GetColorLevel() + (second[0] - first[0])*10)
                self.viewer.Render()

    def on_mousewheel_forward(self, vtk_object, vtk_event):
        self.viewer.GetRenderer().GetActiveCamera().Zoom(1.1)
        self.viewer.Render()
        
    def on_mousewheel_backward(self, vtk_object, vtk_event):
        self.viewer.GetRenderer().GetActiveCamera().Zoom(0.9)
        self.viewer.Render()