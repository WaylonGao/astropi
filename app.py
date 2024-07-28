from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from threading import Thread
from decimal import Decimal

run = True
siderealConst = 100 #Constant for LXD75 RA
m0=1
m1=1
m2=1
currentSpeed = Decimal(1.000) #Speed multiplier


resetPin = 0
sleepPin = 1
stepPin = 2
enablePin = 3
dirPin = 4
m0Pin = 5
m1Pin = 6
m2Pin = 7

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

RA = MotDriver(21,20,26,19,16,13,6,12)
LD = MotDriver(1,2,3,4,5,6,7,8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT) #STEP PIN
GPIO.setup(26, GPIO.OUT) #ENABLE PIN

def step():
    GPIO.output(0, GPIO.HIGH)


def MotorThread():
    global run, currentSpeed

    while True:
        if run:
            T = 1 / (currentSpeed * siderealConst)

        




app = Flask(__name__)



# Define subroutines
def enable_control():
    global currentSpeed
    currentSpeed = round(currentSpeed, 3)
    return f"ENABLED, Running at {currentSpeed}x sidereal"

def disable_control():
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

# Define routes
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

if __name__ == '__main__':
    app.run(debug=True)
