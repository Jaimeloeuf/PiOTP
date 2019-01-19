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

""" Global Variables: """
# Create a new global variable to store sensorData with a initial state of None using the watch class.
sensorData = watch(None)
# Create a new global variable to store interval time between calls to update the sensor data.
intervalTime = watch(30) # Initial value of 30 seconds intervals


# Function to change interval time variable. Interval span can be changed by the User via MQTT
def setIntervalTime(time):
	pass


# Function that will be called every "interval" to update the sensorData and publish the the data to the Broker
def readData():
	# Reference the variable in the global file scope
	global sensorData
	# Read data from sensor and store inside the sensorData object
	sensorData.set(BME.getData())
	# Set the publish topic to 'send', or 'sensor data'
	set_topic('send', 'p')
	# Publish the data to the MQTT Broker
	pub(sensorData.get())


# Call the readData function every "intervalTime" to update the sensor Data and store the reference to this loop in a global variable
intervalTimerRef = setInterval(intervalTime, readData)

# There can only be one timerLoop that calls the readData function in the whole running process to prevent data duplication
# Is there hoisting in python code?


# Set topic to subscribe to.
set_topic("cact", 's')
# Subscribe to the topic that has been set.
sub(parse_payload)







commands = {
	"ac",
	"sd"
}

# The below will be set by the different modes. On setting a new mode, do this
# Every time there is a new data, 
sensorData.addListener()












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




# The below functions are to run as "init" functions when the modes are first set.

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
	# If this is the current running mode, just wait for new incoming commands


def mode_timed():
	pass