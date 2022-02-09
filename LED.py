import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from matplotlib.widgets import Widget
""" import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 26
GPIO.setup(LED, GPIO.OUT) """

class Win(QDialog):

    def __init__(self):
        super(Win,self).__init__()
        loadUi('dialog.ui',self)
        self.setWindowTitle('LED')
        self.btn.clicked.connect(self.on_off)
    
    @pyqtSlot()
    def on_off(self):
        """ if GPIO.input(LED):
            GPIO.output(LED,GPIO.LOW)
            self.btn.setText('OFF')
            self.status.setText('LED : OFF')
        else:
            GPIO.output(LED,GPIO.HIGH)
            self.button.setText('ON')
            self.status.setText('LED : ON') """
        #self.close()
app = QApplication(sys.argv)
widget = Win()
widget.show()
sys.exit(app.exec_())
