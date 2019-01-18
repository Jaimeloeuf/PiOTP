""" 
Module Desciption:
	This module is the code that will be running on the Pi to glue together the operations
	of the MQTT Client lib, the AC controller and the BME sensor interface.

Example code for using the MQTT client lib:
	set_topic("JJ", 'p') # Set publisher topic
	pub('helifgjs') # Publish payload to topic
	sub() # Subscribe to the default topic from the default broker
	pub('helifgjs') # Publish payload to topic

User can pub a message to ask the pi_controller to pub a message about the current state
"""

# Dependencies
# MQTT Client lib
from mqtt import pub, sub, set_broker, set_topic
# from ac import getAC
from data_watcher import watch
# from BME import bme as BME
# from timer import setInterval, t
from datetime import datetime

# Get the AC controller using the function from pi_controller module
ac = getAC()

# Callback function for MQTT subscriptions that parses incoming messages into their individual kv pairs
def parse_payload(payload):
	# Split the payload into their differet key value pairs
	properties = payload.split(';')
	# Loop through each key value pair
	for prop in properties:
		# Split each property into a list with a key and value
		prop = prop.split('=')
		# Verify kv pair and Log out the error if verification failed.
		if not verify(prop):
			print("Error: verification of kv pair from MQTT sub failed.")

# Given the kv pairs parsed out from abv function verify that they are valid?
def verify(prop):
	# Get the key, value pair out of the list
	key = prop[0]
	val = prop[1]
	# Remove white spaces for both the key and value
	for val in prop:
		# See which one works?
		val = val.strip()
		prop[val] = val.strip()
	# If the key is a valid key
	if key in commands:
		if set_state(key, val):
			# If true returned to indicate success, let it bubble up
			return True
	# If set_state returned false or if key not valid, return false to indicate failure
	return False

# Given the kv pairs from abv function set state to the Pi
def set_state(set_this, to_this):
	if set_this == None or to_this == None:
		return False
	elif set_this == 'mode':
		ac.set_mode()

now = datetime.now()
now.date

# Hashmap that will
"""
Every message received in the Topic: 'command+actions' should be a kv pair thing
So the key is the command, and the value is the action or the value or the thing...
E.g.

key is the thing to act upon
value is the action or state that should be applied to the key

ac=on
ac=off
set_sd_interval= # Can set the interval in which the sensor data will be read.
"""
commands = {
	"ac",
	"sd"
}

# Create a new global variable to store sensorData with a initial state of None using the watch class.
sensorData = watch(None)
# Every time there is a new data, 
sensorData.addListener()

""" So based on the global variable, decide what mode it is operating in,
	choose a function for that mode, and apply that as a cb to the addlistener for the sensoor data
	when the variable itself is updated, use a event and callback to change the callback function of the sensor data
	To set a new cb function, use a method to either clear all listeners or remove last listener on the stack,
	before setting the new cb into it.
	

	Make everything into data that is watched so everything will be like node js events
	- Like the brokers and the topics should also be watched so when anything changes, there
	can be event handlers, so you no longer need to set the publisher and broker every single time before publishing data
	when the sensordata changes.
"""

def auto_mode():
	# Control the temperature directly

"""  The different modes
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

def readData(time_interval):
	global sensorData
	# Read data from sensor and store inside the sensorData object
	sensorData.set(BME.getData())
	# Set the publish topic to 'send', or 'send data'
	set_topic('send', 'p')
	# Publish the data to the MQTT Broker
	pub(sensorData.get())


# Call the readData function every 2 minutes to update the sensor Data. Interval span can be changed by the User via MQTT
setInterval((2 * 60), readData)


# Set topic to subscribe to.
set_topic("cact", 's')
# Subscribe to the topic that has been set.
sub(parse_payload)





def set_mode(self, mode):
        if mode == 'auto':
            self.auto('start')
        elif mode == 'man':
            self.auto('stop')
        else:
            return False  # Return false to indicate error and operation failure








    def auto(state):
        # Start and stop the loop based on the state?

        while True:
            if temp > threshold:
                self.off()
            else:
                # Should I put the delay here instead? To test this concept
                self.on(60 * 5)
            # Create async timed loop to control aircon in the background
            await sleep(60 * 5)  # Wait for 5 mins