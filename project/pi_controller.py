""" 
Module Desciption:
	This module is the code that will be running on the Pi to glue together the operations
	of the MQTT Client lib, the AC controller and the BME sensor interface.
	User can pub a message to ask the pi_controller to pub a message about the current state
"""

# Dependencies
# MQTT Client lib
from mqtt import pub, sub, set_broker, set_topic
# Get the AC controller from the ac module.
# from ac import getAC
from data_watcher import watch
# from BME import bme as BME
from timer import setInterval
# from datetime import datetime
# now = datetime.now()
# now.date

"""
Every message received in the Topic: 'command+actions' should be a kv pair thing
So the key is the command, and the value is the action or the value or the thing...
E.g.

key is the thing to act upon
value is the action or state that should be applied to the key

ac=on
ac=off
set_sd_interval= # Can set the interval in which the sensor data will be read.


	So based on the global variable, decide what mode it is operating in,
	choose a function for that mode, and apply that as a cb to the addlistener for the sensoor data
	when the variable itself is updated, use a event and callback to change the callback function of the sensor data
	To set a new cb function, use a method to either clear all listeners or remove last listener on the stack,
	before setting the new cb into it.
	

	Make everything into data that is watched so everything will be like node js events
	- Like the brokers and the topics should also be watched so when anything changes, there
	can be event handlers, so you no longer need to set the publisher and broker every single time before publishing data
	when the sensordata changes.

The different modes
	Data is always read at the given interval and the value is always updated after reading.
	The function for all these modes will just be event handlers that will be called when the value is updated

		sub to the broker's 'man' cmd topic,
		given a new msg that the broker pushed down, do what is requested for
			If the state of the AC is changed, publish the event too.


Man:
	# Do nth but publish the data, the pi_controller should not control the ac directly, only the incoming msg can
	publish the sensor data to the broker
	--> repeat

Auto:
	publish the sensor data to the broker
	Check if the sensor data exceeded the threshold variables
		if exceeded
			change AC state, should there be an on time given? to off the AC after a specified time
			publish above event to broker
		elif below threshold but AC still on:
			off AC
			publish abv event to broker
	--> repeat

Timezone:
	publish the sensor data to the broker
	--> repeat

	(in the background):
	Timer object running, cos the AC is set to on, but with a timeout to off it.


	Implement the watch var class to the AC controller.


 """

 commands = {
	"ac",
	"sd"
}

# Create a new global variable to store sensorData with a initial state of None using the watch class.
sensorData = watch(None)
# Every time there is a new data, 
sensorData.addListener()

def readData():
	global sensorData
	# Read data from sensor and store inside the sensorData object
	sensorData.set(BME.getData())
	# Set the publish topic to 'send', or 'sensor data'
	set_topic('send', 'p')
	# Publish the data to the MQTT Broker
	pub(sensorData.get())


# Call the readData function every 2 minutes to update the sensor Data. Interval span can be changed by the User via MQTT
setInterval((2 * 60), readData)


# Set topic to subscribe to.
set_topic("cact", 's')
# Subscribe to the topic that has been set.
sub(parse_payload)




# Function that returns the different functions to run as eventListeners/background-task when a new mode is used
def change_mode(mode):
	if mode == 'auto':
		return mode_auto
	elif mode == 'man':
		return mode_man
	elif mode == 'timed':
		return mode_timed
	else:
		# Print/Log error
		print('Invalid mode is being passed')
		return False  # Return false to indicate error and operation failure




def mode_auto(state):
	# Start and stop the loop based on the state?

	while True:
		if temp > threshold:
			self.off()
		else:
			# Should I put the delay here instead? To test this concept
			self.on(60 * 5)
		# Create async timed loop to control aircon in the background
		await sleep(60 * 5)  # Wait for 5 mins

def mode_man():
	pass
def mode_timed():
	pass