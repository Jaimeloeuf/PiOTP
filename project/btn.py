""" This module should provide a function, that takes a callback when the button is pressed.
So on btn press, run a function, that should turn the ac on or off """

from gpiozero import Button, Buzzer
from ac import ac

# Create a Button object
btn = Button(pin=23, pull_up=True)

def on_press():
	# Function to toggle state of AC module.
	ac.toggle()
	# Change the operating mode to manual mode too.
	mode

# Setting event listeners for Button input change
btn.when_pressed = on_press