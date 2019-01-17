import MySQLdb
from time import sleep
from gpiozero import LED, PWMLED, Button

led = LED(27)
led.on()
sleep(5);
led.off()
btn = Button(23)
def pressed():
	pass
btn.when_pressed = pressed