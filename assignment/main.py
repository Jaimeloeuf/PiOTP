""" Code for the IOTP Assignment, to basically control the GPIO
	to on and off LEDs when push button is activated """

import RPi.GPIO as GPIO
print(GPIO.RPI_INFO)
mypin = 8
GPIO.setup(mypin, GPIO.OUT, initial=0)

# Put GPIO pin to HIGH state
GPIO.output(mypin, 1)

# Put GPIO pin to LOW state
GPIO.output(mypin, 1)

# Set pin 1 as input
GPIO.setup(1, GPIO.IN, GPIO.PUD_DOWN)

# Print 0 continously until user makes the input pin1 go HIGH
while(True):
	print(GPIO.input(1))

# Clean up GPIO settings to prevent persistent settings from pontentially interferring with other programs
GPIO.cleanup()
# Notify user of program end
print('Program exiting...')
