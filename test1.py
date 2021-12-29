import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'test'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('ON', self)
        button.setToolTip('ON')
        button.move(100,70)
        button.clicked.connect(self.on_click)
        button = QPushButton('OFF', self)
        button.move(100, 90)
        button.resize(button.sizeHint())
        button.clicked.connect(QApplication.instance().quit)
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        #self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
