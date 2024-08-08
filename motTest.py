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

ax = RA
"""
GPIO.setup(ax.resetPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(ax.sleepPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(ax.stepPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ax.enablePin, GPIO.OUT, initial=GPIO.LOW) #LOW to enable
GPIO.setup(ax.dirPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ax.m0Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ax.m1Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ax.m2Pin, GPIO.OUT, initial=GPIO.LOW)
"""
input("HIGH resetpin")
GPIO.setup(ax.resetPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
print("resetPin set to HIGH")

input("LOW enablePin")
GPIO.setup(ax.enablePin, GPIO.OUT, initial=GPIO.LOW) #LOW to enable
print("LOW enablePin")

input("HIGH sleepPin")
GPIO.setup(ax.sleepPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
print("sleepPin set to HIGH")

GPIO.setup(ax.stepPin, GPIO.OUT)
print("stepPin setup")


input("HIGH dirPin")

GPIO.setup(ax.dirPin, GPIO.OUT, initial=GPIO.LOW)
print("dirPin setup HIGH")



def step(motor, period):
    print(f"Stepped period {period}")
    GPIO.output(motor.stepPin, True)
    delay(period / 2)
    GPIO.output(motor.stepPin, False)
    delay(period / 2)

for i in range(40):
    step(RA, 1/4)
print("done")

GPIO.cleanup()