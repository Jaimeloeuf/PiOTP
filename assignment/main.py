""" Code for the IOTP Assignment, to basically control the GPIO
    to on and off LEDs when push button is activated """

# Dependencies
from gpiozero import LED, PWMLED, Button
from time import sleep
from signal import pause

# Using GPIO pin 16 for LED
led = LED(16)
# Using GPIO pin 17 for PWM on LED
led2 = PWMLED(17)
# Using GPIO pin 10 for Buzzer
buzzer = LED(17)
# Using GPIO pin 3 for Button input
button = Button(3)

# Setting event listeners for Button input change
button.when_pressed = led.on
button.when_released = led.off

button.when_pressed = say_hello
def say_hello():
    print('Hello')


while True:
    led2.value = 0  # Output 0% Voltage to GPIO connected to the LED
    sleep(1)
    led2.value = 0.5  # Output 50% Voltage to GPIO connected to the LED
    sleep(1)
    led2.value = 1  # Output 100% Voltage to GPIO connected to the LED
    sleep(1)
    led2.pulse()
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    led.blink()


pause()


# Notify user of program end
print('Program exiting...')


"""
Wait for button to be pressed. Should I make this into a interrupt?
LED and buzzer to activate when button is pressed.

Create a flask server on the pi
Host it on the lan
Access the pi direct via IP on browser
Use the page to toggle LED/Button/Buzzer
Add an encrypt function to the password

Story:
Smart control off apliances
You can off your gas / stove / high wattage device via the 'online portal' for the  server lor
Then you can also monitor the current status of the system. See if it is actually on/off before u toggle them
"""
