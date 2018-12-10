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
"""

# Dependencies
from flask import Flask, render_template, request, abort
from gpiozero import LED, PWMLED, Button
from time import sleep

# Setup
app = Flask(__name__)

# Create an object to maintain the LED state
class State:
    # Assigning default states
    led = [LED(27), LED(22)]  # Using GPIO pin 16 for LED
	pwmLED = PWMLED(17)  # Using GPIO pin 17 for PWM on LED
	buzzer = LED(21)  # Using GPIO pin 10 for Buzzer
	btn = Button(23)  # Using GPIO pin 3 for Button input
	def __init__(self, led, buzz, btn):
		self.btn = btn

    def blinkLED():

	def fadeLED():
		# Create a async timer
		pwmLED.pulse()  # Fade in/out the Red led
	def buzz():
		buzzer.on()
		# Create a async timer
		buzzer.off()


    # Flask server routes
@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')


@app.route('/api/pressed', methods=['POST'])
def get_data():
    handler()
    data = request.get_json()
    hello = data['Hi']
    return hello

# RPI GPIO related

def handler():
    led[0].blink(0.3, 0.3)
    led[1].blink(0.5, 0.5)
    buzzer.on()
    sleep(1)
    buzzer.off()

btn.when_pressed = handler # Setting event listeners for Button input change

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
