"""
This module will expose different funnctions to external API calls to control the PI's
hardware connection through the GPIO
"""
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# import asyncio to allow async sleep/delay operation
from asyncio import sleep


# Setting event listeners for Button input change
# btn.when_pressed = self.btn_pressed_handler
# self.btn = btn

"""
1. Create and initializa a ac controller:
    ac = getAirconController()
2. On ac
    ac.on()
3. Off ac
    ac.off()
4. On ac for a set time asynchrounously.
    ac.on(1000)
"""


class getAirconController:
    # The constructor calls set_pin object method to set pin.
    def __init__(self):
        self.set_pin()  # Call object method to set default pin

    # Method to set pin to be connected to the buzzer other than the default one.
    # GPIO pin 27 will be used for Aircon 'relay' by default
    def set_pin(self, pin=27):
        # Create a digital output controller with the pin arguement
        self.aircon = LED(pin)

    # Method to on the aircon, assuming that the aircon is active high output.
    def on(self, time_on=0):
        # On the aircon
        self.aircon.on()
        # If an on time is specified, wait asynchronously and off the aircon
        if time_on:
            await sleep(time_on)  # Create an async wait timer
            self.aircon.off()

    # Wrapper method over the aircon off function.
    def off(self):
        self.aircon.off()

    def set_mode(self, mode):
        if mode == 'auto':
            self.auto('start')
        elif mode == 'man':
            self.auto('stop')
        else:
            return False  # Return false to indicate error and operation failure

    def auto(state):
        # Start and stop the loop based on the state?

        while True:
            if temp > threshold:
                self.off()
            else:
                # Should I put the delay here instead? To test this concept
                self.on(60 * 5)
            # Create async timed loop to control aircon in the background
            await sleep(60 * 5)  # Wait for 5 mins

    def state(self):
        self.aircon.state()


# Create a function to wrap this inside the state
ac = getAirconController()


def getAC():
    # Function to return the global variable that stores the reference to the ac controller
    return ac


# Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    # print('Error, this module, "pi_state" should not be used as a standalone module')
    exit()
