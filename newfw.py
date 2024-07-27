import time
import network
import socket
from machine import Pin
import utime





#Define INPUT pins:
adjDown = Pin(0, Pin.IN, Pin.PULL_UP)
adjUp = Pin(1, machine.Pin.IN, Pin.PULL_UP)
reverseDir = Pin(2, machine.Pin.IN, Pin.PULL_UP)
enable = Pin(3, machine.Pin.IN, Pin.PULL_UP)

fault = machine.Pin(4, Pin.IN)

#Define OUTPUT LEDs:
pwrLed = machine.Pin(5, Pin.OUT)
stepLed = machine.Pin(6, Pin.OUT)
errorLed = machine.Pin(7, Pin.OUT)


# Define the onboard LED
led = machine.Pin(25, Pin.OUT)

# Define STEPPER DRIVER pins:

resetPin = machine.Pin(8, Pin.OUT)
sleepPin = machine.Pin(9, Pin.OUT)
stepPin = machine.Pin(11, Pin.OUT)
enablePin = machine.Pin(10, Pin.OUT)
dirPin = machine.Pin(12, Pin.OUT)
m2 = machine.Pin(13, Pin.OUT)
m1 = machine.Pin(14, Pin.OUT)
m0 = machine.Pin(15, Pin.OUT)

# Time period for 10Hz frequency (in seconds)
T = 1.0 / 79.5872 #rotate at sidereal rate

on = 1

adjustment = 0.01 #adjustment to T for button presses

enablePin.value(1)
dirPin.value(0)
m0.value(1)
m1.value(1)
m2.value(1)

#Setup sequence

def setup():
    for i in range(15):
        led.toggle()
        print("boop")
        pwrLed.toggle()
        stepLed.toggle()
        errorLed.toggle()
        utime.sleep_ms(100)
        pwrLed.toggle()
        stepLed.toggle()
        errorLed.toggle()
        utime.sleep_ms(100)
    pwrLed.value(1)

    print("Setup done")

setup()     
#turn on enable pin
enablePin.value(0)
dirPin.value(0)
m0.value(1)
m1.value(1)
m2.value(1)
# Main loop

resetPin.value(1)
sleepPin.value(1)
errorLed.value(0)




# Wi-Fi credentials
ssid = 'astroPicoTEST'  # Updated SSID
password = 'bumblebeee'  # Updated password

# Initialize WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP Address:', status[0])

# Function to read HTML file
def read_html():
    try:
        with open('index.html', 'r') as file:
            return file.read()
    except OSError:
        return "Error: index.html file not found"

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

def handle_request(client):
    global T
    request = client.recv(1024)
    request = str(request)
    print('Request:', request)

    if 'led=on' in request:
        led.value(1)
        ledState = "LED is ON"
    elif 'led=off' in request:
        led.value(0)
        ledState = "LED is OFF"
    else:
        ledState = "LED State Unknown"

    if 'command=adjDown' in request:
        print("Web: Adjust Speed Down pressed")
        T = max(T - adjustment, 0.01)  # Ensure T does not become negative
    elif 'command=adjUp' in request:
        print("Web: Adjust Speed Up pressed")
        T += adjustment

    # Check button state
    if button.value() == 1:
        buttonState = "Button is NOT pressed"
    else:
        buttonState = "Button is pressed"
    
    # Create and send response
    stateis = ledState + " and " + buttonState + ", Stepper Speed: %.4f" % T
    html_content = read_html()
    response = html_content % stateis
    client.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
    client.send(response)
    client.close()

# Main loop
while True:
    # Check for web requests
    try:
        client, addr = s.accept()
        print('Client connected from', addr)
        handle_request(client)
    except OSError as e:
        client.close()
        print('Connection closed')
    
    # Stepper control (pseudo-code, needs implementation based on your hardware)
    led.value(1)
    time.sleep(T / 2)
    led.value(0)
    time.sleep(T / 2)

    #Toggle the onboard LED
    led.value(1)
    # Output a square wave on pin 0
    stepPin.value(1)
    utime.sleep(T/2)
    stepPin.value(0)
    led.value(0)

    utime.sleep(T/2)
    

