import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from matplotlib.widgets import Widget
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 26
GPIO.setup(LED, GPIO.OUT) 
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)


class win(QDialog):

    def __init__(self):
        super(win,self).__init__()
        loadUi('dialog.ui',self)
        self.setWindowTitle('LED')
        self.btn_led.clicked.connect(self.led_on)
        self.btn_motor.clicked.connect(self.motor_on)
    
    @pyqtSlot()
    def led_on(self):
        if GPIO.input(LED):
            #condition for led will on
            GPIO.output(LED,GPIO.LOW)
            self.btn_led.setText('OFF')
            self.status_led.setText('LED : OFF')
        else:
            #condition for led will on
            GPIO.output(LED,GPIO.HIGH)
            self.btn_led.setText('ON')
            self.status_led.setText('LED : ON')
        #self.close()

    def motor_on(self):
        #motor on
        self.status_motor.setText('Motor : ON')
        GPIO.output(25,GPIO.LOW)
        GPIO.output(23,GPIO.HIGH)
        #time duration motor on
        time.sleep(3)
        #motor off
        self.status_motor.setText('Motor : OFF')
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)

app = QApplication(sys.argv)
widget = win()
widget.show()
sys.exit(app.exec_())
