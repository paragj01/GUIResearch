import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
ser=GPIO.PWM(8,50)
ser.start(2.5)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'ServoMotor'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        nameLabel = QLabel('Angle',self)
        nameLabel.move(70,40)
        nameLineEdit = QLineEdit(self)
        nameLineEdit.move(130,40)
        nameLabel.setBuddy(nameLineEdit)
        button = QPushButton('ON', self)
        button.move(100,70)
        button.clicked.connect(self.on_click)
        button = QPushButton('OFF', self)
        button.move(100, 90)
        button.clicked.connect(QApplication.instance().quit)
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('click')
        global dc
        deg1 = QLineEdit(self)
        deg = abs(float(deg1))
        dc = 0.056*deg + 2.5
        ser.ChangeDutyCycle(dc)
        print(deg,dc)

        #self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
