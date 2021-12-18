from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(500,200,600,600)
    win.setWindowTitle("Fluid Analysis")
    label = QtWidgets.QLabel(win)
    label.setText("Fluid Analysis")
    label.move(200,200)
    button = QtWidgets.QPushButton(win)
    button.setText("ON/OFF")
    button.move(200,400)


    win.show()
    sys.exit(app.exec_())
window()
