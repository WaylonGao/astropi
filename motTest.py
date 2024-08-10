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

#RA = MotDriver(7,11,13,8,10,12,15,16)
#LD = MotDriver(26,28,19,32,21,36,38,40)





RA = MotDriver(4,17,27,14,15,18, 22,23)
LD = MotDriver(7,1,10,12,9,16,20,21)
drivers = [RA,LD]

GPIO.setmode(GPIO.BCM)

GPIO.setup(LD.resetPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(LD.sleepPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(LD.stepPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LD.enablePin, GPIO.OUT, initial=GPIO.LOW) #LOW to enable
GPIO.setup(LD.dirPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LD.m0Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LD.m1Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LD.m2Pin, GPIO.OUT, initial=GPIO.HIGH)




GPIO.setup(RA.resetPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(RA.sleepPin, GPIO.OUT, initial=GPIO.HIGH) #HIGH TO ENABLE
GPIO.setup(RA.stepPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RA.enablePin, GPIO.OUT, initial=GPIO.LOW) #LOW to enable
GPIO.setup(RA.dirPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RA.m0Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RA.m1Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RA.m2Pin, GPIO.OUT, initial=GPIO.HIGH)

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
    print(f"MOTOR HIGH ON {motor.stepPin}")
    time.sleep(period)
    GPIO.output(motor.stepPin, GPIO.LOW)
    print(f"MOTOR LOW ON {motor.stepPin}")
    time.sleep(period)

    

for i in range(32*600):
    #step(RA, 0.0002)
    step(LD, 0.00001)
    

for i in range(32*600):
    #step(RA, 0.0002)
    step(RA, 0.00001)
print("done")

GPIO.cleanup()