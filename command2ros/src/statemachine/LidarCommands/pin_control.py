from constants import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)


def manual_control():
    while(True):
        if(int(float(input("0 or 1?"))) == 1):
            GPIO.output(SERVO_PIN, GPIO.HIGH)
        else:
            GPIO.output(SERVO_PIN, GPIO.LOW)


def scan_control(scan):
    if scan:
        GPIO.output(SERVO_PIN, GPIO.HIGH)
    else:
        GPIO.output(SERVO_PIN, GPIO.LOW)


manual_control()