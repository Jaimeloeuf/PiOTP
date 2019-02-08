# Dependencies
# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# Timer object to allow task scheduling that runs on another thread
from threading import Timer
# Watch Class used to watch the AC-Controller from tampering
from Jevents import Watch
# JQTT's Publisher Class used to contruct a Publisher for AC state.
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
    5. Toggle the AC's state
        ac.toggle()
    6. Get the current state of the AC module as a Boolean value
        ac.state
"""


class acController:
    """ Class used to build an AC controller object """

    def __init__(self, pin=25):
        """ Takes in optional input for GPIO Pin to use for the 'AC' module """
        # Call set_pin method to set and use default pin
        self.set_pin(pin)
        # Create a instance variable to store Timer Objects
        self.ac_timer = None
        # Create a publisher for the 'ac_state' topic with the Topic prefix.
        self.__pub = Publisher(('IOTP/grp4/channel/ac_state'))

    # Method to set pin to be connected to the buzzer other than the default one.
    def set_pin(self, pin=25):
        # GPIO pin 27 will be used for Aircon 'relay' by default
        # Create digital output with the LED function using pin input arguement
        self.aircon = LED(pin)

    # Method to get current state of the AC. Can be used as a property
    @property
    def state(self):
        # Strictly returns only a value of bool type
        return self.aircon.is_active

    # Method to on the aircon, assuming that the aircon is active high output.
    def on(self, time_on=0):
        # If the aircon is on, and is set to off itself with a Timer
        if self.state and self.ac_timer != None:
            # Stop the timer
            self.ac_timer.cancel()

        # On the aircon if not on already
        if not self.state:
            self.aircon.on()
            # Publish the new state using the magic method
            self.__pub < 'on'

        # If an on time is specified, wait asynchronously and off the aircon
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
        if self.state:
            self.aircon.off()
            # Publish the new state using the magic method
            self.__pub < 'off'

    # Method to toggle the current state of the aircon
    def toggle(self):
        # If there is a Timer in the background running that may interfere with this operation
        if self.ac_timer != None:
            # Stop the timer
            self.ac_timer.cancel()
        # Toggle the current state of the AC
        self.aircon.toggle()
        # Publish the new state using the magic method
        self.__pub < 'on' if self.state else 'off'
        # Return the state of the AC after toggling
        return self.state

    # Magic method to get the current state of the AC module
    __repr__ = state


# Callback function called when the AC controller is changed.
def ac_con_changed():
    print('ERR: AC controller changed.')
    # Should implement the data watcher that uses a loop to constantly hash the object
    # To check for change since this current method relies on the set method being called.

# Put the 'global' ac variable on watch, to prevent other modules or anything from changing its reference without notice
ac_Watcher = Watch(acController())

# Variable that will be exported out to other modules to use to control the AC.
# Give the ac variable the actual AC controller object
ac = ac_Watcher.value

# Set a callback to the Watched object
ac_Watcher.on_set += ac_con_changed


if __name__ == "__main__":
    # Example/Test code to run
    from time import sleep
    
    # On the ac
    ac.on()
    sleep(2)
    
    # Off the ac
    ac.off()
    sleep(2)

    # On the ac, and set it to off after 3 seconds. Note that this is a non-blocking call
    ac.on(3)
    sleep(5)

    # Toggle the current state back to On again
    ac.toggle()
    # Display the current state of the AC module. Should be 'True' here
    print(ac.state)