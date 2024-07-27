from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from threading import Thread
run = True
m0=1
m1=1
m2=1
currentSpeed = 1.0
def MotorThread():
    global run



app = Flask(__name__)



# Define subroutines
def enable_control():
    return f"ENABLED, Running at {currentSpeed}x sidereal"

def disable_control():
    return f"DISABLED"

def sidereal_1x():
    currentSpeed = 1.0
    return "Running at {currentSpeed}x sidereal"

def sidereal_2x():
    currentSpeed = 2.0
    return "Running at {currentSpeed}x sidereal"

def sidereal_5x():
    currentSpeed = 5.0
    return "Running at {currentSpeed}x sidereal"

def sidereal_50x():
    currentSpeed = 50.0
    return "Running at {currentSpeed}x sidereal"

def sidereal_100x():
    currentSpeed = 100.0
    return f"Running at {currentSpeed}x sidereal"

def increment_speed():
    currentSpeed *= 1.1
    return f"Running at {currentSpeed}x sidereal"

def decrement_speed():
    currentSpeed *= 0.9
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
