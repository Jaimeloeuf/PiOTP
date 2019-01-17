import MySQLdb
from time import sleep
from gpiozero import LED, PWMLED, Button

led = LED(27)
led.on()
sleep(5)
led.off()
btn = Button(23)
def pressed():
	pass
btn.when_pressed = pressed

# Below is like a wait, till user press, then program will stop.
raw_input('Press to exit')


# Below is the DB related stuff
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="mydb")
cur = db.cursor()

try:
	cur.execute(""" INSERT INTO store_switch(SN, switch) VALUES ('1', '1') """) # WTF???
	db.commit()
except:
	db.rollback()

cur.close()
db.close()

""" 

<? php
	$pycode = "sudo python /var/www/nameoffile.py";
	$CMD = exec($pycode)
?>


 """