from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from threading import Thread, Event
from decimal import Decimal
import time

GPIO.setwarnings(False)

print("PROGRAM STARTED")

def delay(t):
    time.sleep(float(t))

RAmotor_stop_event = Event()  # Event to control stopping the motor thread
LDmotor_stop_event = Event()  # Event to control stopping the motor thread
RAmotor_thread = None         # Keep track of the motor thread
LDmotor_thread = None         # Keep track of the motor thread
RAcurrentSpeed = Decimal(1.000)  # Speed multiplier
LDcurrentSpeed = Decimal(1.000)  # Speed multiplier

masterPeriod = 1 / 32.1024

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
        self.enabled = False  # Added an enabled flag

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

def step(motor, period):
    GPIO.output(motor.stepPin, True)
    delay(period / 2)
    GPIO.output(motor.stepPin, False)
    delay(period / 2)

app = Flask(__name__)

def enable_control(axis):
    global RAcurrentSpeed, LDcurrentSpeed, RAmotor_stop_event, LDmotor_stop_event, RAmotor_thread, LDmotor_thread
    

    if axis == "RA":
        if RAmotor_thread and motor_thread.is_alive():
            return f"Motor already running at {currentSpeed}x sidereal"
        
        RAmotor_stop_event.clear()  # Clear the event to start the thread
        RAmotor_thread = Thread(target=RAstepperThread, name="RAstepperThread")
        RAmotor_thread.start()
        return f"RA ENABLED, Running at {currentSpeed}x sidereal"
    if axis == "LD":
        if LDmotor_thread and motor_thread.is_alive():
            return f"Motor already running at {currentSpeed}x sidereal"
        
        LDmotor_stop_event.clear()  # Clear the event to start the thread
        LDmotor_thread = Thread(target=RAstepperThread, name="RAstepperThread")
        LDmotor_thread.start()
        return f"LD ENABLED, Running at {currentSpeed}x sidereal"

def disable_control(axis):
    global motor_stop_event, motor_thread
    
    if axis == "RA":
        GPIO.output(RA.enablePin, GPIO.HIGH)
    if axis == "LD":
        GPIO.output(LD.enablePin, GPIO.HIGH)

    #motor_stop_event.set()  # Set the event to signal the thread to stop
    #if motor_thread:
    #    motor_thread.join()  # Wait for the thread to finish
    return f"RA DISABLED"

def sidereal_1x(axis):
    global currentSpeed
    currentSpeed = 1
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_2x(axis):
    global currentSpeed
    currentSpeed = 2
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_5x(axis):
    global currentSpeed
    currentSpeed = 5
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_50x(axis):
    global currentSpeed
    currentSpeed = 50
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def sidereal_100x(axis):
    global currentSpeed
    currentSpeed = 100
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def increment_speed(axis):
    global currentSpeed
    currentSpeed += 0.1
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

def decrement_speed(axis):
    global currentSpeed
    currentSpeed -= 0.1
    currentSpeed = round(currentSpeed, 3)
    return f"Running at {currentSpeed}x sidereal"

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

def RAstepperThread():
    global masterPeriod, currentSpeed, motor_stop_event
    while not motor_stop_event.is_set():
        step(RA, 0.0312 / float(currentSpeed))

if __name__ == "__main__":
    app.run(debug=True)
