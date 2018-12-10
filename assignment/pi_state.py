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