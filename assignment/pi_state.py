# Raspberry Pi GPIO usage dependencies
from gpiozero import LED, PWMLED, Button

# Create an object to maintain the LED state
class State:
    # Assigning default states
    # Using GPIO pin 10 for Buzzer # Using GPIO pin 3 for Button input
    def __init__(self, leds={ green: LED(22), yellow: LED(27), red: LED(27) }, buzzer=LED(21), btn=Button(23)):
        self.leds = leds
        self.buzzer = buzzer
        self.btn = btn

    def set_led(self, state='blink', led=None):
        if state == 'on':
            # Off a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].off()
            else:
                # Else off all leds in the array
                for led in self.leds:
                    led.off()
        elif state == 'off'
            # Off a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].off()
            else:
                # Else off all leds in the array
                for led in self.leds:
                    led.off()
        elif state == 'blink':
            # Blink a specific led in the array of leds if a led is specified by the 'led' variable
            if led != None:
                self.leds[led].blink()
            else:
                # Else make all leds in the array blink
                for led in self.leds:
                    led.blink()
        else:
            print('Error with method call to LED:\nUnrecognised input arguement for "state" parameter')
            return False # Indicate operation failed
        return True # Indicate operation succeded
    def fadeLED(self):
        self.pwmLED.pulse()  # Fade in/out the Red led
    def buzz(self, state=None):
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
            await sleep(1.5) # Create an async wait timer
            self.buzzer.off()
    def get(self, state_of='all'):
        # Construct state based on input arguement and return it to method caller
        if state_of == 'all':
            state = {
                leds: {
                    green: self.leds.green.is_lit(),
                    yellow: self.leds.yellow.is_lit(),
                    red: self.leds.red.is_lit()
                },
                pwmLED: {

                },
                buzzer: state.buzz.is_lit(),
            }
        elif state_of == 'leds':
            state = {

            }
        return state

# Event handler for button pressed
def btn_pressed_handler():
    state.set_led()
    await state.buzz()

# leds[1].blink(0.5, 0.5)
# pwmLED = PWMLED(17)  # Using GPIO pin 17 for PWM on LED

btn.when_pressed = btn_pressed_handler # Setting event listeners for Button input change