from sys import api_version
from PyQt5 import QtCore, QtWidgets, QtGui
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget
import numpy as np
import os
import SimpleITK as sitk

from data import Image
from utils.blend import image_blend
from .Ui_ImageViewer import Ui_ImageViewer
from .WidgetViewer import WidgetViewer, OrientationXY, OrientationXZ, OrientationYZ

class ImageViewer(QtWidgets.QMainWindow, Ui_ImageViewer):
    def __init__(self) -> None:
        super().__init__()
        self.menu_process = None
        self.menu_mcnp = None

        self.image: Image = None
        self.label_colortable: dict = None
        
        self.setupUi(self)
        self.XYwidget = QVTKWidget(self)
        self.YZwidget = QVTKWidget(self)
        self.XZwidget = QVTKWidget(self)
        self.XYviewer = WidgetViewer(qinteractor=self.XYwidget); self.XYviewer.orientation = OrientationXY
        self.YZviewer = WidgetViewer(qinteractor=self.YZwidget); self.YZviewer.orientation = OrientationYZ
        self.XZviewer = WidgetViewer(qinteractor=self.XZwidget); self.XZviewer.orientation = OrientationXZ
        
        self.vtkGridLayout.addWidget(self.XYwidget, 0, 0, 1, 1)
        self.vtkGridLayout.addWidget(self.YZwidget, 0, 1, 1, 1)
        self.vtkGridLayout.addWidget(self.XZwidget, 1, 0, 1, 1)
        self.place_holder = QtWidgets.QLabel()
        self.labelLayout.addWidget(self.place_holder)

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
        self.XYviewer.viewer_initialize()
        self.YZviewer.viewer_initialize()
        self.XZviewer.viewer_initialize()

    def set_connect(self):
        self.spinXY.valueChanged.connect(self.spinSlice_valueChanged)
        self.spinYZ.valueChanged.connect(self.spinSlice_valueChanged)
        self.spinXZ.valueChanged.connect(self.spinSlice_valueChanged)
        self.sliderXY.valueChanged.connect(self.sliderSlice_valueChanged)
        self.sliderYZ.valueChanged.connect(self.sliderSlice_valueChanged)
        self.sliderXZ.valueChanged.connect(self.sliderSlice_valueChanged)
        self.btnOverlay.clicked.connect(self.btnOverlay_clicked)
        self.btnReset.clicked.connect(self.btnReset_clicked)
    
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

    def add_label_colortable(self):
        qplatte = QtGui.QPalette()
        self.labelLayout.removeWidget(self.place_holder)
        for idx, (label_name, setting) in enumerate(self.label_colortable.items()):
            if label_name == "background": continue
            rgb = setting[1]
            name_qlabel = QtWidgets.QLabel()
            name_qlabel.setText(label_name)
            name_qlabel.setFont(QtGui.QFont("微软雅黑", 12))
            color_qlabel = QtWidgets.QLabel()
            qplatte.setColor(QtGui.QPalette.Background, QtGui.QColor(
                int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
            ))
            color_qlabel.setAutoFillBackground(True)
            color_qlabel.setPalette(qplatte)
            self.labelLayout.addWidget(name_qlabel, idx, 0, QtCore.Qt.AlignRight)
            self.labelLayout.addWidget(color_qlabel, idx, 1)
        self.labelLayout.update()

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
            self, "Choose one file", "", "Med File(*.nii *.nii.gz *.mhd)"
        )[0]
        if len(file_name):
            self.image = Image(file_name)
            self.viewer_initialize()
            self.set_spin_slider()
            self.set_voxel()
            self.set_connect()

    @QtCore.pyqtSlot()
    def btnOverlay_clicked(self):
        file_names = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Choose files", "", "Med Files(*.nii *.nii.gz *.mhd)"
        )[0]
        if len(file_names):
            labels = dict()
            for label_file in file_names:
                label_name = os.path.basename(label_file).partition(".")[0]
                label = Image(label_file).array
                if label.shape != self.image.shape:
                    QtWidgets.QMessageBox.warning(self, "Error", "Label shape is not equal to image!")
                    return 
                labels[label_name] = label
            blend_image_array, self.label_colortable = image_blend(self.image.array, labels, alpha=0.3)
            blend_image = sitk.GetImageFromArray(blend_image_array)
            blend_image.CopyInformation(self.image)
            self.XYviewer.label_overlay(blend_image)
            self.XYviewer.set_wlww(127.5, 255.0)
            self.YZviewer.label_overlay(blend_image)
            self.YZviewer.set_wlww(127.5, 255.0)
            self.XZviewer.label_overlay(blend_image)
            self.XZviewer.set_wlww(127.5, 255.0)
            self.add_label_colortable()

    @QtCore.pyqtSlot()
    def btnReset_clicked(self):
        self.XYviewer.reset()
        self.XYviewer.set_wlww(0, 2000)
        self.YZviewer.reset()
        self.YZviewer.set_wlww(0, 2000)
        self.XZviewer.reset()
        self.XZviewer.set_wlww(0, 2000)

        while True:
            item = self.labelLayout.takeAt(0)
            if item is not None: 
                item.widget().deleteLater()
            else:
                break
        self.labelLayout.addWidget(self.place_holder)
        self.labelLayout.update()
            
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