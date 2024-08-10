from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from threading import Thread
from decimal import Decimal
import time

GPIO.setwarnings(False)

print("PROGRAM STARTED")

def delay(t):
    time.sleep(float(t))

motor_enabled = False  # Global flag to control the motor thread
siderealConst = 100 #Constant for LXD75 RA
m0=1
m1=1
m2=1
currentSpeed = Decimal(1.000) #Speed multiplier

masterPeriod=1/32.1024

resetPin = 0
sleepPin = 1
stepPin = 2
enablePin = 3
dirPin = 4
m0Pin = 5
m1Pin = 6
m2Pin = 7

class MotDriver:
    def __init__(self, dirPin, stepPin, sleepPin, resetPin, m2Pin, m1Pin, m0Pin, enablePin, name):
        self.resetPin = resetPin
        self.sleepPin = sleepPin
        self.stepPin = stepPin
        self.enablePin = enablePin
        self.dirPin = dirPin
        self.m0Pin = m0Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin
        self.name = name

RA = MotDriver(4,17,27,14,15,18, 22,23, "Right Ascension")
LD = MotDriver(7,1,10,12,9,16,20,21, "Left Declination")

drivers = [RA,LD]

GPIO.setmode(GPIO.BCM)

for d in drivers:
    GPIO.setup(d.resetPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.sleepPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.stepPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.enablePin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.dirPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.m0Pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.m1Pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.m2Pin, GPIO.OUT, initial=GPIO.HIGH)

def step(motor, period):
    GPIO.output(motor.stepPin, True)
    delay(period / 2)
    GPIO.output(motor.stepPin, False)
    delay(period / 2)

app = Flask(__name__)

def enable_control():
    global currentSpeed, motor_enabled
    motor_enabled = True
    Thread(target=stepperThread, name="stepperThread").start()  # Start the thread when enabled
    return f"ENABLED, Running at {currentSpeed}x sidereal"

def disable_control():
    global motor_enabled
    motor_enabled = False  # Stop the motor by setting the flag to False
    return f"DISABLED"

def sidereal_1x():
    global currentSpeed
    currentSpeed = 1
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_2x():
    global currentSpeed
    currentSpeed = 2
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_5x():
    global currentSpeed
    currentSpeed = 5
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_50x():
    global currentSpeed
    currentSpeed = 50
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_100x():
    global currentSpeed
    currentSpeed = 100
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def increment_speed():
    global currentSpeed
    currentSpeed += 0.1
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def decrement_speed():
    global currentSpeed
    currentSpeed -= 0.1
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

@app.route('/', methods=['GET'])
def index():
    status = ""
    if 'control' in request.args:
        if request.args['control'] == 'on':
            status = enable_control()
        elif request.args['control'] == 'off':
            status = disable_control()
    elif 'command' in request.args:
        if request.args['command'] == 'sidereal1x':
            status = sidereal_1x()
        elif request.args['command'] == 'sidereal2x':
            status = sidereal_2x()
        elif request.args['command'] == 'sidereal5x':
            status = sidereal_5x()
        elif request.args['command'] == 'sidereal50x':
            status = sidereal_50x()
        elif request.args['command'] == 'sidereal100x':
            status = sidereal_100x()
        elif request.args['command'] == 'increment':
            status = increment_speed()
        elif request.args['command'] == 'decrement':
            status = decrement_speed()
    
    return render_template('index.html', status=status)

def stepperThread():
    global masterPeriod, currentSpeed, motor_enabled
    while motor_enabled:
        step(RA, 0.0312 / float(currentSpeed))
        time.sleep(0.01)  # Allow the loop to be interrupted

if __name__ == "__main__":
    app.run(debug=True)
