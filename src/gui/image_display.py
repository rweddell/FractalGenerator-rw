from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QPixmap


class ImageLabel(qtw.QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(qtc.Qt.AlignCenter)

        # TODO: ....
        self.setText('\n\n Drop an image \n\n')
        self.setStyleSheet('''
                QLabel{
                    border: 4px dashed #aaa
                }
            ''')
        
    def setPixmap(self, image):
        super().setPixmap(image)

class DropWidget(qtw.QWidget):

    pic_dropped = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)
        mainLayout = qtw.QVBoxLayout()
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(qtc.Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()
            self.pic_dropped.emit(file_path)
        else:
            event.ignore()
    
    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))