from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from threading import Thread
from decimal import Decimal

run = True
m0=1
m1=1
m2=1
currentSpeed = Decimal(1.000)
def MotorThread():
    global run



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
