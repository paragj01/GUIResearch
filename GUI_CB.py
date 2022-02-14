# This Python file uses the following encoding: utf-8
#import os
#from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
#from PySide6.QtCore import QFile
from PyQt5.uic import loadUi
#from PySide6.QtUiTools import QUiLoader
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 26
GPIO.setup(LED, GPIO.OUT)
Motor =25 
GPIO.setup(Motor, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.load_ui()
        loadUi('dialog.ui',self)
        self.btnled.clicked.connect(self.led_on)
        self.btnmotor.clicked.connect(self.motor_on)
        self.comboBox.clicked.connect(self.combo_box)
        #self.btntype.clicked.connect(self.btn_type)
        #self.typetime.clicked.connect(self.type_time)

    """ def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close() """
    
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
    
    def combo_box (self):
        #add items to the combobox
        self.comboBox.addItem("Python")
        self.comboBox.addItem("Java")
        self.comboBox.addItem("C++")
        self.comboBox.addItem("C#")
        self.comboBox.addItem("JavaScript")
 
        #connected combobox signal
        self.comboBox.currentTextChanged.connect(self.combo_selected)
    
    def combo_selected(self):
        item = self.combo.currentText()
        self.label_cb.setText("You selected : " + item)

    """ def type_time(self):
        self.close

    def btn_type(self):
        self.close """

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
