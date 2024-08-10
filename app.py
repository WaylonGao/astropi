from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from decimal import Decimal
import time

GPIO.setwarnings(False)

print("PROGRAM STARTED")

def delay(t):
    time.sleep(float(t))

RAcurrentSpeed = Decimal(1.000)  # Speed multiplier for RA
LDcurrentSpeed = Decimal(1.000)  # Speed multiplier for LD

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

RA = MotDriver(4, 17, 27, 14, 15, 18, 22, 23, "Right Ascension")
LD = MotDriver(7, 1, 10, 12, 9, 16, 20, 21, "Left Declination")

drivers = [RA, LD]

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

def enable_control(axis):
    if axis == "RA":
        GPIO.output(RA.enablePin, GPIO.LOW)
        return f"RA ENABLED"
    elif axis == "LD":
        GPIO.output(LD.enablePin, GPIO.LOW)
        return f"LD ENABLED"
    return "UNKNOWN AXIS"

def disable_control(axis):
    if axis == "RA":
        GPIO.output(RA.enablePin, GPIO.HIGH)
        return f"RA DISABLED"
    elif axis == "LD":
        GPIO.output(LD.enablePin, GPIO.HIGH)
        return f"LD DISABLED"
    return "UNKNOWN AXIS"

def sidereal_1x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 1
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 1
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

def sidereal_2x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 2
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 2
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

def sidereal_5x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 5
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 5
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

def sidereal_50x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 50
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 50
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

def sidereal_100x(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed = 100
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed = 100
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

def increment_speed(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed += Decimal('0.1')
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed += Decimal('0.1')
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

def decrement_speed(axis):
    if axis == "RA":
        global RAcurrentSpeed
        RAcurrentSpeed -= Decimal('0.1')
        return f"RA Running at {RAcurrentSpeed}x sidereal"
    elif axis == "LD":
        global LDcurrentSpeed
        LDcurrentSpeed -= Decimal('0.1')
        return f"LD Running at {LDcurrentSpeed}x sidereal"
    return "UNKNOWN AXIS"

@app.route('/', methods=['GET'])
def index():
    status = ""
    axis = request.args.get('axis')
    
    if 'control' in request.args:
        if request.args['control'] == 'on':
            status = enable_control(axis)
        elif request.args['control'] == 'off':
            status = disable_control(axis)
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

if __name__ == "__main__":
    app.run(debug=True)
