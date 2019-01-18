""" 
Module Desciption:
	This module is the code that will be running on the Pi to glue together the operations
	of the MQTT Client lib, the AC controller and the BME sensor interface.

Example code:
	set_topic("JJ", 'p') # Set publisher topic
	pub('helifgjs') # Publish payload to topic
	sub() # Subscribe to the default topic from the default broker
	pub('helifgjs') # Publish payload to topic

User can pub a message to ask this to pub a message about the current state
"""

# Dependencies
from mqtt import pub, sub, set_broker, set_topic
from ac import getAC
from BME import bme as BME
from timer import setInterval, t
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


def readData(time_interval):
	# Set the publish topic to 'send', or 'send data'
	set_topic('send', 'p')
	# Read and publish the data via the MQTT lib
	# Only publish the data if the value changes?
	pub(BME.getData())


# Every 2 minutes, read the data from the BME sensor. The time span can be changed by the User
setInterval((2 * 60), readData)


# Set topic to subscribe to.
set_topic("cact", 's')
# Subscribe to the topic that has been set.
sub(parse_payload)