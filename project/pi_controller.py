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
class getBuzzer:
    # The constructor will use GPIO pin 22 for Buzzer by default
    def __init__(self, pin=22):
        self.set_pin(pin) # Call object method to set pin

    # Method to set pin to be connected to the buzzer other than the default one.
    def set_pin(self, pin=22):
        # Create a digital output controller with the input pin
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



# Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    # print('Error, this module, "pi_state" should not be used as a standalone module')
    exit()
