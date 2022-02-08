import sys

from PyQt5 import QtCore, QtWidgets, QtSerialPort 
from PyQt5.QtWidgets import (QApplication, QMainWindow ,QWidget ,QToolBar ,QHBoxLayout, QAction ,QStatusBar ,
                                QLineEdit ,QPushButton ,QTextEdit , QVBoxLayout, QStyledItemDelegate, QGridLayout, QMessageBox, QFrame)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt , pyqtSignal
from PyQt5.QtSerialPort import QSerialPortInfo

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # set window name
        self.setWindowTitle("Centre for Microsystems")

        # set status bar
        self.status = self.statusBar()
        self.status.showMessage("Centre for Microsystems")

        # set the initial window size
        self.setFixedSize(600, 400)

        # settings icon
        self.setWindowIcon(QIcon("icon.png"))

                

        #close event
    """ def closeEvent(self, event):
        result = QMessageBox.question(self, 'Leaving...','Do you want to exit?', QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:

            event.accept()  
        else:
            event.ignore() """
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())