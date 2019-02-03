# Dependencies
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# Timer object to allow task scheduling that runs on another thread
from threading import Timer
from Jevents import Watch
from JQTT import Publisher


""" This module exposes different funnctions to control the hardware with the Pi's GPIO.

    Code Examples
    1. Get the single AC controller
        from ac import ac
    2. On ac
        ac.on()
    3. Off ac
        ac.off()
    4. On ac for a set time asynchrounously.
        ac.on(1000)
"""


class acController:
    # Single timer object to keep track of time.
    ac_timer = None

    def __init__(self, pin=27):
        """ Takes in optional input for GPIO Pin to use for the 'AC' module """
        # Call set_pin method to set and use default pin
        self.set_pin(pin)
        # Create a publisher for the 'ac_state' topic
        self.__pub = Publisher('ac_state')

    # Method to set pin to be connected to the buzzer other than the default one.
    def set_pin(self, pin=27):
        # GPIO pin 27 will be used for Aircon 'relay' by default
        # Create digital output with the LED function using pin input arguement
        self.aircon = LED(pin)

    # Method to on the aircon, assuming that the aircon is active high output.
    def on(self, time_on=0):
        # On the aircon if not on already
        if self.state() == 'off':
            self.aircon.on()
            # Publish the new state
            self.__pub += 'on'  # Pub using the magic method

        # If an on time is specified, wait asynchronously and off the aircon
        # if time_on != None and self.ac_timer != None:
        if time_on:
            # If there is any timer stored previously, stop and overwrite it.
            if self.ac_timer != None:
                self.ac_timer.cancel()
            # Create and start a timer object to call the self.off method on timeout.
            self.ac_timer = Timer(time_on, self.off)
            self.ac_timer.start()

    # Wrapper method over the aircon off function.
    def off(self):
        # Off the aircon if currently on
        if self.state() == 'on':
            self.aircon.off()
            # Publish the new state
            self.__pub += 'off'  # Pub using the magic method

    # Method to get current state of the AC. Can be used as a property
    @property
    def state(self):
        self.aircon.state()


# Variable that will be exported out to other modules to use to control the AC.
# Put the 'global' ac variable on watch, to prevent other modules or anything from changing its reference without notice
ac = Watch(acController()).value

# Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    exit()

    # Should change this to run a test or example code instead
