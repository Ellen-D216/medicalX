from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
import os
import SimpleITK as sitk

from data import Image
from utils.blend import image_blend
from .Ui_ImageViewer import Ui_ImageViewer

class ImageViewer(QtWidgets.QMainWindow, Ui_ImageViewer):
    def __init__(self) -> None:
        super().__init__()

        self.image: Image = None
        self.blend_image: Image = None
        self.label_colortable: dict = None
        
        self.setupUi(self)
        self.imageGrid = QtWidgets.QGridLayout()
        self.actor.setLayout(self.imageGrid)
        self.XYimv = pg.ImageView(self.actor)
        self.YZimv = pg.ImageView(self.actor)
        self.XZimv = pg.ImageView(self.actor)
        self.imageGrid.addWidget(self.XYimv, 0, 0)
        self.imageGrid.addWidget(self.YZimv, 0, 1)
        self.imageGrid.addWidget(self.XZimv, 1, 0)

        self.actionOpen_Folder.triggered.connect(self.btnOpenFolder_clicked)
        self.actionOpen_File.triggered.connect(self.btnOpenFile_clicked)

    def set_connect(self):
        self.actionOverlay_Labels.triggered.connect(self.btnOverlay_clicked)
        self.actionReset.triggered.connect(self.btnReset_clicked)
        # self.YZroi.sigRegionChanged.connect(self.roi_change)
        # self.XZroi.sigRegionChanged.connect(self.roi_change)

    # def add_label_colortable(self):
    #     qplatte = QtGui.QPalette()
    #     self.labelLayout.removeWidget(self.place_holder)
    #     for idx, (label_name, setting) in enumerate(self.label_colortable.items()):
    #         if label_name == "background": continue
    #         rgb = setting[1]
    #         name_qlabel = QtWidgets.QLabel()
    #         name_qlabel.setText(label_name)
    #         name_qlabel.setFont(QtGui.QFont("微软雅黑", 12))
    #         color_qlabel = QtWidgets.QLabel()
    #         qplatte.setColor(QtGui.QPalette.Background, QtGui.QColor(
    #             int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
    #         ))
    #         color_qlabel.setAutoFillBackground(True)
    #         color_qlabel.setPalette(qplatte)
    #         self.labelLayout.addWidget(name_qlabel, idx, 0, QtCore.Qt.AlignRight)
    #         self.labelLayout.addWidget(color_qlabel, idx, 1)
    #     self.labelLayout.update()

    def set_image(self, image:Image):
        image_array = image.array#.swapaxes(1, 2)
        channel = image_array.shape[-1] if len(image_array.shape) == 4 else None

        xy_scale = [image.spacing[0]/image.spacing[1], 1]
        self.XYimv.setImage(image_array, scale=xy_scale, axes={'t':0, 'x':2, 'y':1, 'c':channel})

        yz_scale = [image.spacing[2]/image.spacing[1], 1]
        self.YZimv.setImage(image_array, scale=yz_scale, axes={'t':2, 'x':1, 'y':0, 'c':channel})
        
        xz_scale = [image.spacing[2]/image.spacing[0], 1]
        self.XZimv.setImage(image_array, scale=xz_scale, axes={'t':1, 'x':2, 'y':0, 'c':channel})
        
    @QtCore.pyqtSlot()
    def btnOpenFolder_clicked(self):
        file_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose one folder", ""
        )
        if len(file_directory):
            self.image = Image(file_directory)
            self.set_image(self.image)
            self.set_connect()

    @QtCore.pyqtSlot()
    def btnOpenFile_clicked(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose one file", "", "Med File(*.nii *.nii.gz *.mhd)"
        )[0]
        if len(file_name):
            self.image = Image(file_name)
            self.set_image(self.image)
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
            self.blend_image = Image(blend_image_array); self.blend_image.CopyInformation(self.image)
            self.set_image(self.blend_image)
            
    @QtCore.pyqtSlot()
    def btnReset_clicked(self):
        self.set_image(self.image)
        