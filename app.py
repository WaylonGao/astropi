from flask import Flask, request, render_template, redirect, url_for
import RPi.GPIO as GPIO
from threading import Thread, Event
from decimal import Decimal
import time
import os
import math
import json

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

class Target:
    def __init__(self, RA, LD, name = ""):
        self.RA = RA
        self.LD = LD
        self.name = name

RA = MotDriver(4, 17, 27, 14, 15, 18, 22, 23, "Right Ascension")
LD = MotDriver(7, 1, 10, 12, 9, 16, 20, 21, "Left Declination")

currentTarget = Target("","","")
currentPos = Target("","","")

drivers = [RA, LD]

# GPIO setup
GPIO.setmode(GPIO.BCM)

for d in drivers:
    GPIO.setup(d.resetPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.sleepPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.stepPin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.enablePin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(d.dirPin, GPIO.OUT, initial=GPIO.LOW) #LOW for sidereal
    GPIO.setup(d.m0Pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.m1Pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(d.m2Pin, GPIO.OUT, initial=GPIO.HIGH)

def setMotorDirection(motor, direction):
    if direction == "fwd":
        GPIO.output(motor.dirPin, GPIO.LOW)
    if direction == "rev":
        GPIO.output(motor.dirPin, GPIO.HIGH)


def setMicrostepping(motor, resolution):
    #Resolution can be from the following: 1,2,4,8,16,32
    match resolution:
        case 1:
            GPIO.output(motor.m0Pin, GPIO.LOW)
            GPIO.output(motor.m1Pin, GPIO.LOW)
            GPIO.output(motor.m2Pin, GPIO.LOW)
        case 2:
            GPIO.output(motor.m0Pin, GPIO.HIGH)
            GPIO.output(motor.m1Pin, GPIO.LOW)
            GPIO.output(motor.m2Pin, GPIO.LOW)
        case 4:
            GPIO.output(motor.m0Pin, GPIO.LOW)
            GPIO.output(motor.m1Pin, GPIO.HIGH)
            GPIO.output(motor.m2Pin, GPIO.LOW)
        case 8:
            GPIO.output(motor.m0Pin, GPIO.HIGH)
            GPIO.output(motor.m1Pin, GPIO.HIGH)
            GPIO.output(motor.m2Pin, GPIO.LOW)
        case 16:
            GPIO.output(motor.m0Pin, GPIO.LOW)
            GPIO.output(motor.m1Pin, GPIO.LOW)
            GPIO.output(motor.m2Pin, GPIO.HIGH)
        case 32:
            GPIO.output(motor.m0Pin, GPIO.HIGH)
            GPIO.output(motor.m1Pin, GPIO.HIGH)
            GPIO.output(motor.m2Pin, GPIO.HIGH)


def HMStoDeg(hms):
    """
    Convert a right ascension coordinate in 'hh h mm m' format to degrees.

    Args:
    hms (str): A string in the format 'hh h mm m', e.g. '03h 47.0m'

    Returns:
    float: The equivalent angle in degrees.
    """
    # Split the input string into components
    parts = hms.split()
    
    # Extract hours and minutes
    hours = float(parts[0].replace('h', ''))
    minutes = float(parts[1].replace('m', ''))
    
    # Convert hours and minutes to degrees
    degrees = (hours * 15) + (minutes / 60 * 15)
    
    return degrees

def DMStoDeg(dms):
    """
    Convert a declination in '+ddº mm’' format to decimal degrees.

    Args:
    dms (str): A string in the format '+ddº mm’', e.g. '+24º 07’'

    Returns:
    float: The equivalent angle in decimal degrees.
    """
    # Split the input string into degrees and minutes
    parts = dms.split()
    
    # Extract degrees and minutes
    degrees = float(parts[0].replace('º', ''))
    minutes = float(parts[1].replace('’', ''))
    
    # Convert minutes to degrees
    decimal_degrees = degrees + (minutes / 60)
    
    return decimal_degrees

def stepTrim(num):
    return math.floor(num * 10) / 10


def goToThread(motor, delta):
    deltaMajor = stepTrim(delta) #The largest movement to fullstep
    deltaMinor = delta - deltaMajor #The small bit to microstep

    #First, make the major delta movement (full steps)
    setMicrostepping(motor, 1) #Set motor to full steps

    StepsToTake = deltaMajor * 240 #240 steps per output degree

    for i in range (StepsToTake):
        step(motor, 0.01)

    time.sleep(0.01)

    setMicrostepping(motor, 32) #Set motor to 1/32 microsteps
    angleRotated = deltaMajor
    while angleRotated < delta:
        step(motor, 0.0001)
        angleRotated += 0.01667 #1 1/32step = 0.01667 deg output
        #Microstep the rest of the way
    
    print("ARRIVED AT DESTINATION")
    exit #Exit the thread
    



def goTo():
    global currentPos, currentTarget
    ##First calculate angle difference between the two
    #currentTarget - currentPos
    print(f"currentPos: {currentPos}")
    print(f"currentTarget: {currentTarget}")
    raDelta= currentTarget.RA - HMStoDeg(currentPos.RA)
    ldDelta= currentTarget.LD - DMStoDeg(currentPos.LD)
    Thread(target=goToThread(RA, raDelta)).start()
    Thread(target=goToThread(LD, ldDelta)).start()
    


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
    disable_control(RA)
    disable_control(LD)
    os.system("sudo shutdown -h now")

def reboot():
    disable_control(RA)
    disable_control(LD)
    os.system("sudo shutdown -r now")

def restartProgram():
    disable_control(RA)
    disable_control(LD)
    os.system("sudo systemctl stop flaskapp && sleep 1 && sudo systemctl start flaskapp")

def updateProgram():
    disable_control(RA)
    disable_control(LD)
    os.system("sudo systemctl stop flaskapp && git pull && sudo systemctl start flaskapp")


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
    global currentTarget, currentPos
    status = ""
    
    axis = request.args.get('axis')
    if not axis:
        return render_template('index.html', status="No axis selected")

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
        elif request.args['command'] == 'shutdown':
            # Redirect to home and schedule shutdown
            status = "Redirecting to home before shutdown..."
            Thread(target=shutdown).start()
            return redirect(url_for('index'))
        elif request.args['command'] == 'reboot':
            # Redirect to home and schedule reboot
            status = "Redirecting to home before reboot..."
            Thread(target=reboot).start()
            return redirect(url_for('index'))
        elif request.args['command'] == 'restartprogram':
            # Redirect to home and schedule shutdown
            status = "Redirecting to home before program restart..."
            Thread(target=restartProgram).start()
            return redirect(url_for('index'))
        elif request.args['command'] == 'updateprogram':
            # Redirect to home and schedule reboot
            status = "Redirecting to home before program update..."
            Thread(target=updateProgram).start()
            return redirect(url_for('index'))
        

        elif request.args['command'] == 'selectOrion':
            #global currentTarget, currentPos
            status = "ORION nebula selected"
            
            currentTarget.RA = HMStoDeg("03h 47.0m")
            currentTarget.LD = DMStoDeg("+24º 07’")
            currentTarget.name = "M42 Orion Nebula"

            goTo()
            currentPos=currentTarget
            #RA 03h 47.0m, LD. +24º 07’
            return redirect(url_for('index'))
        
        elif request.args['command'] == 'goHome':
            
            status = "HOME position selected"

            currentTarget.RA = HMStoDeg("00h 00.0m")
            currentTarget.LD = DMStoDeg("+00º 00’")
            currentTarget.name = "Home position"

            goTo()
            currentPos=currentTarget
            return redirect(url_for('index'))
        

    
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
