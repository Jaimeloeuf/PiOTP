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
from flask import Flask, render_template, request, abort, jsonify
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# import asyncio
from asyncio import sleep

# Setup
app = Flask(__name__)
    # pwmLED = PWMLED(17)  # Using GPIO pin 17 for PWM on LED

# Create an object to maintain the LED state
class State:
    # Assigning default states
    # Using GPIO pin 10 for Buzzer # Using GPIO pin 3 for Button input
    def __init__(self, leds={ green: LED(22), yellow: LED(27), red: LED(27) }, buzzer=LED(21), btn=Button(23)):
        self.leds = leds
        self.buzzer = buzzer
        self.btn = btn

    def set_led(self, blink='blink', led=None):
        if blink == 'blink':
            # Blink a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].blink()
            else:
                # Else make all leds in the array blink
                for led in self.leds:
                    led.blink()
        elif blink == 'on'
            # Off a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].off()
            else:
                # Else off all leds in the array
                for led in self.leds:
                    led.off()
        elif blink == 'off'
            # Off a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].off()
            else:
                # Else off all leds in the array
                for led in self.leds:
                    led.off()
        else:
            print('Error with method call to LED:\nUnrecognised input arguement for "blink" parameter')
    def fadeLED(self):
        self.pwmLED.pulse()  # Fade in/out the Red led
    def buzz(self, set=None):
        # If 'set' is set, use it to manually control state. Else do a auto buzz
        if set != None:
            if set == 'on':
                self.buzzer.on()
            elif set == 'off':
                self.buzzer.off()
            else:
                print('Error with method call to buzz:\nUnrecognised input arguement for "set" parameter')
        else:
            self.buzzer.on()
            await sleep(1.5) # Create an async wait timer
            self.buzzer.off()


# 'Global' object that maintains state
state = State()

# Status object that will be serialized into JSON before being sent back to the client
# Below is the initial state of the program
status = {
    leds: {
        green: state.leds.green.is_lit(),
        yellow: state.leds.yellow.is_lit(),
        red: state.leds.red.is_lit()
    },
    pwmLED: {

    },
    buzzer: state.buzz.is_lit(),
}

    # Flask server routes
@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')


@app.route('/api/get/state', methods=['GET'])
def current_state():
    # return jsonify({ 'State': status })
    return jsonify(status)


# led APIs
@app.route('/api/<color>/get', methods=['GET'])
def index(color):


@app.route('/api/<color>/<state>', methods=['POST'])
def set_state(color, state):
    # Smth like react, where I set the state variable. Which is actually just a 'shadow state', which will look at the diff and update the real state
    return render_template('./index.html')



def btn_pressed_handler():
    state.set_led()
    await state.buzz()


# Route to mimic pressing the button
@app.route('/api/press_btn', methods=['POST'])
def get_data():
    btn_pressed_handler()
    # Below is a simple echo function
    data = request.get_json()
    return data

# leds[1].blink(0.5, 0.5)

btn.when_pressed = btn_pressed_handler # Setting event listeners for Button input change

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
