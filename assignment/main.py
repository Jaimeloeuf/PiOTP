"""
Description:
Code for IOTP Assignment

Program flow:
1.  Wait for button to be pressed.  /  Wait for a POST requests at the /api/pressed route
2.  Call handler function to respond
    2.1 Red LED fades with PWM.
    2.2.  Yellow and Green LED Blinks
    2.3.  Quick fire buzzer for 2 seconds
    2.4.  Stop everything after 5 seconds
3.  Echo the JSON data back to the client if handler is called because of the POST request


buzz function will be called at every action
"""

# Dependencies
# Server dependencies
from flask import Flask, render_template, request, abort
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# import asyncio
from asyncio import sleep

# Setup
app = Flask(__name__)

# Create an object to maintain the LED state
class State:
    # Assigning default states
    # Using GPIO pin 16 for LED
    pwmLED = PWMLED(17)  # Using GPIO pin 17 for PWM on LED
    # Using GPIO pin 10 for Buzzer
    # Using GPIO pin 3 for Button input
    leds = {
        green: LED(22),
        yellow: LED(27),
        red: LED(27),
    }

    def __init__(self, leds=[LED(27), LED(22)], buzz=LED(21), btn=Button(23)):
        self.leds = leds
        self.buzz = buzz
        self.btn = btn

    def LED(self, blink='blink', led=None):
        if blink == 'blink':
            # Blink a specific led in the array of leds if the position is specified in the led variable
            if led != None:
                self.leds[led].blink()
            else:
                # Else make all leds in the array blink
                for led in self.leds:
                    led.blink()
        elif blink == 'stop'

    def fadeLED(self):
        self.pwmLED.pulse()  # Fade in/out the Red led
    def buzz(self):
        self.buzzer.on()
        await sleep(1.5) # Create an async wait timer
        self.buzzer.off()

# 'Global' object that maintains state
state = State()


# Status object that will be serialized into JSON before being sent back to the client
# Below is the initial state of the program
status = {
    leds: {
        green: 'off',
        yellow: 'off',
        red: 'off'
    },
    pwmLED: {

    },
    buzzer: 'off'
}

    # Flask server routes
@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')

# led APIs
@app.route('/api/green/get', methods=['GET'])
def index():

@app.route('/api/yellow/get', methods=['GET'])
def index():

@app.route('/api/red/get', methods=['GET'])
def index():



@app.route('/api/green/on', methods=['POST'])
def green():
    return render_template('./index.html')

@app.route('/api/yellow/on', methods=['POST'])
def yellow():
    return render_template('./index.html')

@app.route('/api/red/on', methods=['POST'])
def red():
    return render_template('./index.html')


@app.route('/api/green/off', methods=['POST'])
def green():
    return render_template('./index.html')

@app.route('/api/yellow/off', methods=['POST'])
def yellow():
    return render_template('./index.html')

@app.route('/api/red/off', methods=['POST'])
def red():
    return render_template('./index.html')


# Route to mimic pressing the button
@app.route('/api/press_btn', methods=['POST'])
def get_data():
    data = request.get_json()
    hello = data['Hi']
    return hello

# leds[1].blink(0.5, 0.5)

btn.when_pressed = handler # Setting event listeners for Button input change

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
