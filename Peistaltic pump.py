import RPi.GPIO as GPIO
import time

from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO.output(25,GPIO.LOW)
GPIO.output(23,GPIO.HIGH)

time.sleep(0.3)

GPIO.output(25,GPIO.HIGH)
GPIO.output(23,GPIO.HIGH)
