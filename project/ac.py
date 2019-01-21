# Dependencies
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# Timer object to allow task scheduling that runs on another thread
from threading import Timer
from data_watcher import watch
from JQTT import pub, set_topic

# Setting event listeners for Button input change
# btn.when_pressed = self.btn_pressed_handler
# self.btn = btn

""" @Docs
    This module will expose different funnctions to external API calls to control the PI's
    hardware connection through the GPIO.


    @Code Examples
    1. Get the single AC controller
        ac = getAC()
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
        # On the aircon if not on already
        if self.state() == 'off':
            self.aircon.on()
            # Set publish topic and publish
            set_topic('ac_state', 'p')
            pub('on')
            
        # If an on time is specified, wait asynchronously and off the aircon
        if time_on and self.ac_timer != None:
            # Create a timer object to call the self.off method after timeout
            self.ac_timer = Timer(time_on, self.off)

    # Wrapper method over the aircon off function.
    def off(self):
        # Off the aircon if currently on
        if self.state() == 'on':
            self.aircon.off()
            # Set publish topic and publish
            set_topic('ac_state', 'p')
            pub('off')

    def state(self):
        self.aircon.state()


# Variable that will be exported out to other modules to use to control the AC.
# ac = acController()
# Put the 'global' ac variable on watch, to prevent other modules or anything from changing its reference without notice
ac = watch(acController()).get()

# Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    exit()