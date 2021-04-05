import RPi.GPIO as GPIO
import time

# set up vibrating motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

# setting vibration time
GPIO.output(4, GPIO.HIGH)
time.sleep(2)
GPIO.output(4, GPIO.LOW)
GPIO.output(4, GPIO.HIGH)
time.sleep(2)
GPIO.output(4, GPIO.LOW)
GPIO.output(4, GPIO.HIGH)
time.sleep(2)
GPIO.output(4, GPIO.LOW)
