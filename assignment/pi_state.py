# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button
# import asyncio to allow async sleep/delay operation
from asyncio import sleep

async def off_leds(leds, onTime):
    if onTime > 0:
        await sleep(onTime) # Create an async wait timer
        if isinstance(leds, list):
            # Off leds one by one if it is a list that was passed in
            for led in leds:
                led.off()
        else:
            leds.off()

# Class to maintain the state of the Pi's GPIO pins
class State:
    # Default states: GPIO pin 10 for Buzzer ; GPIO pin 3 for Button input ..etc..
    def __init__(self, leds={ 'green': LED(22), 'yellow': LED(27), 'red': LED(27) }, buzzer=LED(21), btn=Button(23)):
        self.leds = leds
        self.buzzer = buzzer
        btn.when_pressed = self.btn_pressed_handler # Setting event listeners for Button input change
        self.btn = btn

    def set_new_led(self, name, pin, pwm=False):
        if (name == None) or (pin == None):
            print('Error with method call to new_led:\nUnrecognised input arguement for either "name" or "pin" parameter')
            return False # Return false to indicate operation failed
        for led in leds:
            if led.pin == pin
                print('Error with method call to set_new_led:\nPin "%s" already in use', pin)
                return False
        if self.btn.pin == pin:
            print('Error with method call to set_new_led:\nPin "%s" already in use', pin)
            return False
        if self.buzzer.pin == pin:
            print('Error with method call to set_new_led:\nPin "%s" already in use', pin)
            return False

        self.leds[name] = PWMLED(pin) if pwm else LED(pin)
        return True # Indicate operation succeded
        
    async def set_led(self, state='blink', led=None, onTime=0):
        if state == 'on':
            # Off a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].on()
                await off_leds(self.leds[led], onTime)
            else:
                # Else off all leds in the array
                for led in self.leds:
                    led.on()
                await off_leds(self.leds, onTime)
        elif state == 'blink':
            # Blink a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].blink()
                await off_leds(self.leds[led], onTime)
            else:
                # Else make all leds in the array blink
                for led in self.leds:
                    led.blink()
                await off_leds(self.leds, onTime)
        elif state == 'off':
            # Off a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].off()
            else:
                # Else off all leds in the array
                for led in self.leds:
                    led.off()
        else:
            print('Error with method call to LED:\nUnrecognised input arguement for "state" parameter')
            return False # Indicate operation failed
        return True # Indicate operation succeded

    def fadeLED(self, led):
        if self.leds[led] == None:
            print('Error with method call to fadeLED:\nUnrecognised input arguement for "led" parameter')
            return False
        # Convert the led into a PWM Led
        # self.leds[led].PWMLED
        # self.pwmLED.pulse()  # Fade in/out the Red led

    def set_buzzer(self, pin):
        # Can directly call the buzzer variable from the object, but this method provides a safety check
        if pin == None:
            print('Error with method call to set_buzzer:\nUnrecognised input arguement for "pin" parameter')
            return False # Return false to indicate operation failed
        for led in leds:
            if led.pin == pin
                # Disable the LED control thing and change it to buzzer
                print('Error with method call to set_buzzer:\nPin "%s" already in use', pin)
                return False
        if self.btn.pin == pin:
            print('Pin "%s" now used for ', pin)
            return False
        self.buzzer = LED(pin)
        return True # Indicate operation succeded

    async def buzz(self, state=None, onTime=0):
        # If 'state' is set, use it to manually control state. Else do a auto buzz
        if state != None:
            if state == 'on':
                self.buzzer.on()
            elif state == 'off':
                self.buzzer.off()
            else:
                print('Error with method call to buzz:\nUnrecognised input arguement for "state" parameter')
        else:
            self.buzzer.on()
            await sleep(onTime if (onTime > 0) else 1.5) # Create an async wait timer with 1.5 default wait time
            self.buzzer.off()

    def get(self, state_of='all'):
        # Construct state based on input arguement and return it to method caller
        if state_of == 'all':
            return {
                'leds': {
                    'green': self.leds.green.is_lit(),
                    'yellow': self.leds.yellow.is_lit(),
                    'red': self.leds.red.is_lit()
                },
                'buzzer': self.buzzer.is_lit()
            }
        elif state_of == 'leds':
            return {
                'green': self.leds.green.is_lit(),
                'yellow': self.leds.yellow.is_lit(),
                'red': self.leds.red.is_lit()
            }
        elif state_of == 'buzzer':
            return { 'buzzer': self.buzzer.is_lit() }
        else:
            print('Error with method call to get:\nUnrecognised input arguement for "state_of" parameter')

    # Event handler for button pressed
    def btn_pressed_handler(self):
        self.set_led() # To edit
        await self.buzz()

# Error checking code to prevent running this module as it is.
if __name__ == "__main__":
    print('Error, this module, "%s" should not be used as a standalone module' % __name__)
    # print('Error, this module, "pi_state" should not be used as a standalone module')
    exit()



# leds[1].blink(0.5, 0.5)
# pwmLED = PWMLED(17)  # Using GPIO pin 17 for PWM on LED


# Avail GPIO pins to use: 0 - 27
# btn use din,
# pwm use dout
# led and buzzer both uses dout
use = ['din', 'dout', 'ain', 'aout', 'led', 'pwm', 'buzzer']
So the setting thing takes in a name and a pin usage type and the pin number
def set_pin(name, pin_num, use):
    # Input Error checking
    if (pin_num < 0) or (pin_num > 27):
        print('Error Invalid pin number to assign')
        exit()
    
    if pins.get(name, pin_num): # if the pin has already been used.
        print('Choosing "N" will cause program to quit')
        while True:
            option = input('Set new function for name / pin number used? (Y/N): ')
            if option == 'y' or option == 'Y':
                break
            elif option == 'n' or option == 'N':
                exit()
            else:
                print('Invalid input. Try again')
    pins.set(name, pin_num, use)