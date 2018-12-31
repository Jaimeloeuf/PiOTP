""" Dependencies """
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# import asyncio to allow async sleep/delay operation
# from asyncio import sleep


""" Avail GPIO pins to use: 0 - 27
	btn use i,
	fading led use pwm,
	led and buzzer both uses o.

The main difference between my Abstraction API and just using the official gpiozero API is that my one maintains a map of the entire GPIO state. And it allows u to just get the entire state and modifiy multiple things directly. Like the ability to set multiple digital pins high at the same time / off all GPIO

To create a 'disable GPIO' function to so called off everything but rmb the state of the pins before it was offed, in order to conserve power and allow the GPIO state to be reapplied at a later stage.
Something like using GIT STASH to store current unsaved modified state!

When user set a pin or make a change to the state, update the physical state and record the change into the state object.
The state will then store 27 Pin objects
 """

# leds[1].blink(0.5, 0.5)
# pwmLED = PWMLED(17)  # Using GPIO pin 17 for PWM on LED

set_pin(22, 'o', 'led1')
state('led1', 'on')
state('led1', 'off')
state('led1', 'blink', 70)  # 70% Duty cycle ratio

def set_pin(pin_num, use, name):
    # Input Error checking
    if (pin_num < 0) or (pin_num > 27):
        print('Error Invalid pin number to assign')
        exit()  # Should I call exit or just throw an error?

    if pins.get(name, pin_num):  # if the pin has already been used.
        print('Choosing "N" will cause program to quit')
        while True:
            option = input(
                'Set new function for name / pin number used? (Y/N): ')
            if option == 'y' or option == 'Y':
                break
            elif option == 'n' or option == 'N':
                exit()
            else:
                print('Invalid input. Try again')
    pins.set(name, pin_num, use)
    Pin(use, pin_num, name)


class Pin:
	uses = ['i', 'o', 'pwm'] # Default Usage ways for the pins. Input/Output/PWM-output all are digital.
	names = {}
	# Constructor takes in the pin number, a pin usage type and optionally a name to call that pin directly
    def __init__(self, pin_num, use='o', name):
		# Do a check before setting usage
		for usecase in uses:
			if use == usecase:
				self.use = use
		else:
			# throw error

		# Do a check before setting name
		for used_name in names:
			if name = used_name:
				# Throw error
		else:
			self.name = name


class state:
    stash = []
    state = {}
    # Get current state of GPIO

    def get(self):
        return self.state

    # Stash the current state
    def stash(self):
        self.stash.push(self.state)
        return len(self.stash)

    # apply the state stored in stash
    # To make stash into a object by itself with functions
    def apply(self):
        self.set_state(self.stash.pop())
        return True  # Indicate a OK
    # Set all the pins at once. Allow some bitmasking?

    def set_state(self, state):
		# The state will be a ascii text thing
        self.state = state

    def set_pin(self, *args):
        # each arg is a key value pair

        # Allow some use of decorators where user can just add their own functions to control state

     # Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    # print('Error, this module, "pi_state" should not be used as a standalone module')
    exit()