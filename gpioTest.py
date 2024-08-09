##GPIO TESTING UTILITY

import RPi.GPIO as g
import time as t

g.setmode(g.BCM)
g.setwarnings(False)
def test(pin):
    g.setup(pin, g.OUT)
    g.output(pin, g.LOW)
    t.sleep(1)
    g.output(pin, g.HIGH)
    t.sleep(1)
    
while True:
    a = int(input("enter test pin:"))
    if a > 100:
        print("EXITING")
        break
    else:
        print(f"Testing pin {a}")
        test(a)
        print(f"Succesfully tested pin {a}")

