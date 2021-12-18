from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(500,200,200,200)
    win.setWindowTitle("Test Window")
    label = QtWidgets.QLabel(win)
    label.setText("LED Light")
    label.move(100,100)
    button = QtWidgets.QPushButton(win)
    button.setText("ON/OFF")
    button.move(100,150)


    win.show()
    sys.exit(app.exec_())
window()
