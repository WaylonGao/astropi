from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from threading import Thread, Event
from decimal import Decimal
import time
import os

# Initialize Flask app
app = Flask(__name__)

GPIO.setwarnings(False)

print("PROGRAM STARTED")

def delay(t):
    time.sleep(float(t))

# Events to control stopping the motor threads
RAmotor_stop_event = Event()
LDmotor_stop_event = Event()

# Speed multipliers
RAcurrentSpeed = Decimal(1.000)
LDcurrentSpeed = Decimal(1.000)

masterPeriod = 1 / 32.1024


# Define motor driver pins
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
        self.enabled = False

RA = MotDriver(4, 17, 27, 14, 15, 18, 22, 23, "Right Ascension")
LD = MotDriver(7, 1, 10, 12, 9, 16, 20, 21, "Left Declination")

drivers = [RA, LD]

# GPIO setup
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

# Motor stepping function
def step(motor, period):
    GPIO.output(motor.stepPin, True)
    delay(period / 2)
    GPIO.output(motor.stepPin, False)
    delay(period / 2)

# Control functions
def enable_control(axis):
    if axis == "RA":
        GPIO.output(RA.enablePin, GPIO.LOW)
        return "RA ENABLED"
    elif axis == "LD":
        GPIO.output(LD.enablePin, GPIO.LOW)
        return "LD ENABLED"

def disable_control(axis):
    if axis == "RA":
        GPIO.output(RA.enablePin, GPIO.HIGH)
        return "RA DISABLED"
    elif axis == "LD":
        GPIO.output(LD.enablePin, GPIO.HIGH)
        return "LD DISABLED"
    
def shutdown():
    os.system("sudo shutdown -h now")

def reboot():
    os.system("sudo shutdown -r now")


# Speed adjustment functions
def sidereal_1x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 1
        return "RA Running at 1x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 1
        return "LD Running at 1x sidereal"

def sidereal_2x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 2
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 2
        return f"LD Running at {LDcurrentSpeed}x sidereal"

def sidereal_5x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 5
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 5
        return f"LD Running at {LDcurrentSpeed}x sidereal"

def sidereal_50x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 50
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 50
        return f"LD Running at {LDcurrentSpeed}x sidereal"

def sidereal_100x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 100
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 100
        return f"LD Running at {LDcurrentSpeed}x sidereal"

def increment_speed(axis):
    if axis == "RA":
        RAcurrentSpeed += Decimal(0.1)
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        LDcurrentSpeed += Decimal(0.1)
        return f"LD Running at {LDcurrentSpeed}x sidereal"

def decrement_speed(axis):
    if axis == "RA":
        RAcurrentSpeed -= Decimal(0.1)
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        LDcurrentSpeed -= Decimal(0.1)
        return f"LD Running at {LDcurrentSpeed}x sidereal"

# Route definitions
@app.route('/', methods=['GET'])
def index():
    status = ""
    
    axis = request.args.get('axis')
    if not axis:
        return render_template('index.html', status="No axis selected")

    if 'control' in request.args:
        if request.args['control'] == 'on':
            status = enable_control(axis)
        elif request.args['control'] == 'off':
            status = disable_control(axis)
    if 'sysctl' in request.args:
        if request.args['control'] == 'shutdown':
            status = "SHUTTING DOWN"
            shutdown()
        elif request.args['control'] == 'reboot':
            status = "REBOOTING"
            reboot()
    elif 'command' in request.args:
        if request.args['command'] == 'sidereal1x':
            status = sidereal_1x(axis)
        elif request.args['command'] == 'sidereal2x':
            status = sidereal_2x(axis)
        elif request.args['command'] == 'sidereal5x':
            status = sidereal_5x(axis)
        elif request.args['command'] == 'sidereal50x':
            status = sidereal_50x(axis)
        elif request.args['command'] == 'sidereal100x':
            status = sidereal_100x(axis)
        elif request.args['command'] == 'increment':
            status = increment_speed(axis)
        elif request.args['command'] == 'decrement':
            status = decrement_speed(axis)
    
    return render_template('index.html', status=status)


# Stepper thread functions
def RAstepperThread():
    global RAcurrentSpeed
    while True:
        step(RA, 0.0312 / float(RAcurrentSpeed))

def LDstepperThread():
    global LDcurrentSpeed
    while True:
        step(LD, 0.0312 / float(LDcurrentSpeed))

# Start the motor threads
RAmotor_thread = Thread(target=RAstepperThread, name="RAstepperThread")
RAmotor_thread.start()
LDmotor_thread = Thread(target=LDstepperThread, name="LDstepperThread")
LDmotor_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
