import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

print("PROGRAM STARTED")

def delay(t):
    time.sleep(float(t))


run = True
siderealConst = 100 #Constant for LXD75 RA
m0=1
m1=1
m2=1


masterPeriod=32


class MotDriver:
    def __init__(self, resetPin, sleepPin, stepPin, enablePin, dirPin, m0Pin, m1Pin, m2Pin):
        self.resetPin = resetPin
        self.sleepPin = sleepPin
        self.stepPin = stepPin
        self.enablePin = enablePin
        self.dirPin = dirPin
        self.m0Pin = m0Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin

RA = MotDriver(14,27,17,23,4,22,18,15)
LD = MotDriver(12,25,1,21,7,20,16,9)

drivers = [RA,LD]

GPIO.setmode(GPIO.BCM)


for d in drivers:
    GPIO.setup(d.resetPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.sleepPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.stepPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.enablePin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.dirPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.m0Pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.m1Pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.m2Pin, GPIO.OUT, initial=GPIO.LOW)
    

def step(motor, period):
    print(f"Stepped period {period}")
    GPIO.output(motor.stepPin, True)
    delay(period / 2)
    GPIO.output(motor.stepPin, False)
    delay(period / 2)


while True:
    step(RA, 1/4)