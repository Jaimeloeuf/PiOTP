from threading import Timer
"""
This module is the code that will be running on the Pi to glue together the operations
of the MQTT Client lib, the AC controller and the BME sensor interface.
"""

from mqtt import pub, sub, set_broker, set_topic
from pi_controller import getAirconController
from datetime import datetime

""" Example code:

	set_topic("JJ/is", 'p') # Set publisher topic
	pub('helifgjs') # Publish payload to topic
	sub() # Subscribe to the default topic from the default broker
	pub('helifgjs') # Publish payload to topic

User can pub a message to ask this to pub a message about the current state
"""

# Set topic to subscribe to.
set_topic("JJ/IOTP/cact", 's')
# Subscribe to the topic that has been set.
sub()


def parse_payload(payload="kgh"):
    # Split the payload into their differet key value pairs
    properties = payload.split(';')
    # Loop through each key value pair
    for prop in properties:
        # Split each property into a list with a key and value
        prop = prop.split('=')
        # Remove white spaces for both the key and value
        for val in prop:
            val = val.strip()
            set_stuff(prop)


def set_stuff(prop):
    # Get the key value pair out of the list
    key = prop[0]
    val = prop[1]
    # If the key is a valid key
    if key in commands:
		if set_state(key, value):
			# If true returned to indicate success, let it bubble up
			return True
	# If set_state returned false or if key not valid, return false to indicate failure
	return False


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
"""
commands = {

}


# Every 2 minutes, read the data from the BME sensor. The time span can be changed by the User
readData_timer = Timer(2*60, BME.getData)
readData_timer.start()
