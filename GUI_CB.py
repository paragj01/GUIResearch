import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QDoubleValidator
from PyQt5.uic import loadUi
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 26
GPIO.setup(LED, GPIO.OUT)
Motor = 25 
GPIO.setup(Motor, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.load_ui()
        loadUi('/home/pi/Desktop/GUI/Ui/form.ui',self)
        self.btnled.clicked.connect(self.led_on)
        self.btnmotor.clicked.connect(self.motor_on)
        self.spinBox.valueChanged.connect(self.spin_box)
        self.btnsubmit.clicked.connect(self.combo_box)
        
    def led_on(self):
        if GPIO.input(LED):
            #condition for led will on
            GPIO.output(LED,GPIO.LOW)    
            self.btnled.setText('OFF')
        else:
            #condition for led will on
            GPIO.output(LED,GPIO.HIGH)
            self.btnled.setText('ON')
    
    def motor_on(self):
        #motor on
        self.btnmotor.setText('ON')
        GPIO.output(25,GPIO.LOW)
        GPIO.output(23,GPIO.HIGH)
        #time duration motor on
        time.sleep(1)
        #motor off
        self.btnmotor.setText('OFF')
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)
        
    def spin_box (self):
        value = self.spinBox.value()
        self.labelsb.setText("Value : " + str(value))
        #self.btntype.clicked.connect(self.motor_btn)
        #motor on
        self.btnmotor.setText('ON')
        GPIO.output(25,GPIO.LOW)
        GPIO.output(23,GPIO.HIGH)
        #time duration motor on
        time.sleep(value)
        #motor off
        self.btnmotor.setText('OFF')
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)

    def combo_box(self):
        item = self.comboBox.currentText()
        self.labelcb.setText("You selected : " + item)
        
if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
