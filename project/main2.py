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


def parse_payload(payload="kgh"):
    # Split the payload into their differet key value pairs
    properties = payload.split(';')
    # Loop through each key value pair
    for prop in properties:
        # Split each property into a list with a key and value
        prop = prop.split('=')
        # Remove white spaces
        for val in prop:
            val = val.strip()


def set_stuff(prop):
    # Get the key value pair out of the list
    key = prop[0]
    val = prop[1]
    # If the key is a valid key


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

ac on
ac off 
"""
commands = {

}


# Every 2 minutes, read the data from the BME sensor. The time span can be changed by the User
from threading import Timer
readData_timer = Timer(2*60, BME.getData)
readData_timer.start()