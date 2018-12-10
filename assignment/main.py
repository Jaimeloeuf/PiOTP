"""
Description:
Code for IOTP Assignment

Program flow:
1.  Wait for button to be pressed.  /  Wait for a POST requests at the /api/press_btn route
2.  Call handler function to respond
    2.1 Red LED fades with PWM.
    2.2.  Yellow and Green LED Blinks
    2.3.  Quick fire buzzer for 2 seconds
    2.4.  Stop everything after 5 seconds
3.  Echo the JSON data back to the client if handler is called because of the POST request
"""
# Dependencies
# Server dependencies
from flask import Flask, render_template, request, abort, jsonify
# Import the state controller from pi_state module that I wrote
from pi_state import State

# 'Global' object that holds a State object thath maintains state of the RaspPi's GPIO pins
state = State()
# 'Global' object for Flask server
app = Flask(__name__)

# Flask server routes

@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')

@app.route('/api/get/state', methods=['GET'])
def current_state():
    # The returned 'state' object will be serialized into JSON before being sent back to the client
    # return jsonify({ 'State': status })
    return jsonify(state.get())

# led APIs
@app.route('/api/led/<color>/get', methods=['GET'])
def get_led_state(color):
    if state.leds[color] != None:
        return jsonify({ color: state.leds[color] })

# Smth like react, where I set the state variable. Which is actually just a 'shadow state', which will look at the diff and update the real state
@app.route('/api/led/<color>/set/<state>', methods=['POST'])
def set_led_state(color, state):
    if state.leds[color] != None:
        if state.set_led(state=state, led=color):
            return jsonify({ color: state.leds[color] })
        else:
            return 'Invalid request failed'

# Flask Route to mimic pressing the button
@app.route('/api/press_btn', methods=['POST'])
def get_data():
    state.btn_pressed_handler()
    # Below is a simple echo function
    data = request.get_json()
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)