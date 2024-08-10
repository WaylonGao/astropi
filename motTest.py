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
    def __init__(self, dirPin, stepPin, sleepPin, resetPin, m2Pin, m1Pin, m0Pin, enablePin):
        self.resetPin = resetPin
        self.sleepPin = sleepPin
        self.stepPin = stepPin
        self.enablePin = enablePin
        self.dirPin = dirPin
        self.m0Pin = m0Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin

RA = MotDriver(7,11,13,8,10,12,15,16)
LD = MotDriver(26,28,19,32,21,36,38,40)

drivers = [RA,LD]

GPIO.setmode(GPIO.BOARD)

ax = RA

GPIO.setup(ax.resetPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(ax.sleepPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(ax.stepPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ax.enablePin, GPIO.OUT, initial=GPIO.LOW) #LOW to enable
GPIO.setup(ax.dirPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ax.m0Pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(ax.m1Pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(ax.m2Pin, GPIO.OUT, initial=GPIO.HIGH)

input("start:")

def step1(motor, period):
    print(motor.stepPin)
    print(f"Stepped period {period}")
    GPIO.output(motor.stepPin, GPIO.HIGH)
    delay(period / 2)
    
    GPIO.output(motor.stepPin, GPIO.LOW)
    delay(period / 2)

def step(motor, period):
    
    GPIO.output(motor.stepPin, GPIO.HIGH)
    print(f"MOTOR LOW ON {motor.stepPin}")
    time.sleep(period)
    GPIO.output(motor.stepPin, GPIO.LOW)
    print(f"MOTOR LOW ON {motor.stepPin}")
    time.sleep(period)

    

for i in range(20):
    step(RA, 1)
print("done")

GPIO.cleanup()