"""
Description:
Code for IOTP Assignment

Program flow:
1.  Wait for button to be pressed.
2.  Red LED fades with PWM.
3.  Yellow and Green LED Blinks
4.  Quick fire buzzer for 2 seconds
5.  Stop everything after 5 seconds


Create a flask server on the pi
Host it on the lan
Access the pi direct via IP on browser
Use the page to toggle LED/Button/Buzzer
Add an encrypt function to the password

Story:
Smart control off apliances
You can off your gas / stove / high wattage device via the 'online portal' for the  server lor
Then you can also monitor the current status of the system. See if it is actually on/off before u toggle them
"""


# Dependencies
from flask import Flask, render_template, abort, request
from gpiozero import LED, PWMLED, Button
from time import sleep
# from signal import pause

# Setup
app = Flask(__name__)
led = [LED(27), LED(22)] # Using GPIO pin 16 for LED
pwmLED = PWMLED(17) # Using GPIO pin 17 for PWM on LED
buzzer = LED(23) # Using GPIO pin 10 for Buzzer
btn = Button(3) # Using GPIO pin 3 for Button input

# Flask server routes
@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')

@app.route('/api/switch', methods=['POST'])
def get_data():
    data = request.get_json()
    return data

    # abort(404)

# RPI GPIO related
# Setting event listeners for Button input change
btn.when_pressed = handler
btn.when_released = led.off

def handler():
    pwmLED.pulse() # Fade in/out the Red led
    led[0].blink(0.5, 0.5)
    led[1].blink(0.5, 0.5)

# pause()
# Notify user of program end
print('Program exiting...')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)