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
1. Create and initializa a buzzer:
    buzzer = getBuzzer()

2. On buzzer
    buzzer.on()

3. Off buzzer
    buzzer.off()
4. On buzzer for a set time asynchrounously.
    buzzer.on(1000)
"""


class getBuzzerController:
    # The constructor calls set_pin object method to set pin.
    def __init__(self, pin):
        self.set_pin(pin)  # Call object method to set pin

    # Method to set pin to be connected to the buzzer other than the default one.
    # GPIO pin 22 will be used for Buzzer by default
    def set_pin(self, pin=22):
        # Create a digital output controller with the pin arguement
        self.buzzer = LED(pin)

    # Method to on the buzzer, assuming that the buzzer is active high output.
    def on(self, time_on=0):
        # On the buzzer
        self.buzzer.on()
        # If an on time is specified, wait asynchronously and off the buzzer
        if time_on:
            await sleep(time_on)  # Create an async wait timer
            self.buzzer.off()

    # Wrapper method over the buzzer off function.
    def off(self):
        self.buzzer.off()


class getAirconController:
    # The constructor calls set_pin object method to set pin.
    def __init__(self, pin):
        self.set_pin(pin)  # Call object method to set pin

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

    def state(self):
        self.aircon.state()


# Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    # print('Error, this module, "pi_state" should not be used as a standalone module')
    exit()
