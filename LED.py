import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSlot
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
LED = 8
GPIO.setup(LED, GPIO.OUT)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'LED'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        button = QPushButton(self)
        button.move(100,70)
        button.clicked.connect(self.on_off)

    @pyqtSlot()
    def on_off(self):
        if GPIO.input(LED):
            GPIO.output(LED,GPIO.LOW)
            self.button.setText('OFF')

        else:
            GPIO.input(LED)
            GPIO.output(LED,GPIO.HIGH)
            self.button.setText('ON')

        #self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
