import sys 
from .ImageViewer import ImageViewer
from PyQt5.QtWidgets import QApplication

def gui_start():
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.show()
    sys.exit(app.exec_())