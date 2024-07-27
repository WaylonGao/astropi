from flask import Flask, request, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# Define subroutines
def enable_control():
    return "control enabcontrol"

def disable_control():
    return "control disabcontrol"

def sidereal_1x():
    return "Sidereal 1x activated"

def sidereal_2x():
    return "Sidereal 2x activated"

def sidereal_5x():
    return "Sidereal 5x activated"

def sidereal_50x():
    return "Sidereal 50x activated"

def sidereal_100x():
    return "Sidereal 100x activated"

def increment_speed():
    return "Speed incremented by 0.1x"

def decrement_speed():
    return "Speed decremented by 0.1x"

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
