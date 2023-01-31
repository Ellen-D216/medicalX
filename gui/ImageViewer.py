from PyQt5 import QtCore, QtWidgets, QtGui
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget
import numpy as np
import os

from .Ui_ImageViewer import Ui_ImageViewer
from data import Image
from utils.viewer import Viewer, OrientationXY, OrientationXZ, OrientationYZ

class ImageViewer(QtWidgets.QMainWindow, Ui_ImageViewer):
    def __init__(self) -> None:
        super().__init__()
        self.menu_process = None
        self.menu_mcnp = None

        self.image: Image = None
        
        self.setupUi(self)
        self.XYwidget = QVTKWidget(self)
        self.YZwidget = QVTKWidget(self)
        self.XZwidget = QVTKWidget(self)
        self.XYviewer = Viewer(interactor=self.XYwidget); self.XYviewer.orientation = OrientationXY
        self.YZviewer = Viewer(interactor=self.YZwidget); self.YZviewer.orientation = OrientationYZ
        self.XZviewer = Viewer(interactor=self.XZwidget); self.XZviewer.orientation = OrientationXZ
        self.vtkGridLayout.addWidget(self.XYwidget, 0, 0, 1, 1)
        self.vtkGridLayout.addWidget(self.YZwidget, 0, 1, 1, 1)
        self.vtkGridLayout.addWidget(self.XZwidget, 1, 0, 1, 1)

        self.leVoxelNum.setReadOnly(True)
        self.leVoxelSize.setReadOnly(True)
        self.sliderXY.setSingleStep(10)
        self.sliderXY.setPageStep(1)
        self.sliderYZ.setSingleStep(10)
        self.sliderYZ.setPageStep(1)
        self.sliderXZ.setSingleStep(10)
        self.sliderXZ.setPageStep(1)

        self.btnOpenFolder.clicked.connect(self.btnOpenFolder_clicked)
        self.btnOpenFile.clicked.connect(self.btnOpenFile_clicked)
        # self.actionChangeSetting.triggered.connect(self.actionChangeSetting_clicked)


    def viewer_initialize(self):
        self.XYviewer.set_image_data(self.image)
        self.YZviewer.set_image_data(self.image)
        self.XZviewer.set_image_data(self.image)

        self.XYviewer.initialize()
        self.YZviewer.initialize()
        self.XZviewer.initialize()

    def set_connect(self):
        self.spinXY.valueChanged.connect(self.spinSlice_valueChanged)
        self.spinYZ.valueChanged.connect(self.spinSlice_valueChanged)
        self.spinXZ.valueChanged.connect(self.spinSlice_valueChanged)
        self.sliderXY.valueChanged.connect(self.sliderSlice_valueChanged)
        self.sliderYZ.valueChanged.connect(self.sliderSlice_valueChanged)
        self.sliderXZ.valueChanged.connect(self.sliderSlice_valueChanged)
    
    def set_spin_slider(self):
        self.spinXY.setRange(0, self.image.size[2]-1)
        self.spinYZ.setRange(0, self.image.size[0]-1)
        self.spinXZ.setRange(0, self.image.size[1]-1)
        self.spinXY.setValue(self.image.size[2]//2)
        self.spinYZ.setValue(self.image.size[0]//2)
        self.spinXZ.setValue(self.image.size[1]//2)
        
        self.sliderXY.setRange(0, self.image.size[2]-1)
        self.sliderYZ.setRange(0, self.image.size[0]-1)
        self.sliderXZ.setRange(0, self.image.size[1]-1)
        self.sliderXY.setValue(self.image.size[2]//2)
        self.sliderYZ.setValue(self.image.size[0]//2)
        self.sliderXZ.setValue(self.image.size[1]//2)

    def set_voxel(self):
        self.leVoxelNum.setText(
            f"{self.image.size[0]}×{self.image.size[1]}×{self.image.size[2]}"
        )
        self.leVoxelSize.setText(
            f"{self.image.spacing[0]:.3f}×{self.image.spacing[1]:.3f}×{self.image.spacing[2]:.3f} mm"
        )

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        self.XYwidget.Finalize()
        self.YZwidget.Finalize()
        self.XZwidget.Finalize()

    @QtCore.pyqtSlot()
    def btnOpenFolder_clicked(self):
        file_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose one folder", ""
        )
        if len(file_directory):
            self.image = Image(file_directory)
            self.viewer_initialize()
            self.set_spin_slider()
            self.set_voxel()
            self.set_connect()

    @QtCore.pyqtSlot()
    def btnOpenFile_clicked(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose one file", ""
        )[0]
        if len(file_name):
            self.image = Image(file_name)
            self.viewer_initialize()
            self.set_spin_slider()
            self.set_voxel()
            self.set_connect()

    @QtCore.pyqtSlot()
    def spinSlice_valueChanged(self):
        sender = self.sender()
        if sender == self.spinXY:
            value = self.spinXY.value()
            self.sliderXY.setValue(value)
            self.XYviewer.set_slice(value)
        elif sender == self.spinYZ:
            value = self.spinYZ.value()
            self.sliderYZ.setValue(value)
            self.YZviewer.set_slice(value)
        elif sender == self.spinXZ:
            value = self.spinXZ.value()
            self.sliderXZ.setValue(value)
            self.XZviewer.set_slice(value)

    @QtCore.pyqtSlot()
    def sliderSlice_valueChanged(self):
        sender = self.sender()
        if sender == self.sliderXY:
            value = self.sliderXY.value()
            self.spinXY.setValue(value)
            self.XYviewer.set_slice(value)
        elif sender == self.sliderYZ:
            value = self.sliderYZ.value()
            self.spinYZ.setValue(value)
            self.YZviewer.set_slice(value)
        elif sender == self.sliderXZ:
            value = self.sliderXZ.value()
            self.spinXZ.setValue(value)
            self.XZviewer.set_slice(value)