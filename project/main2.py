from mqtt import pub, sub, set_broker, set_topic

# Set publisher topic
set_topic("JJ/is", 'p')
# Publish payload to topic
pub('helifgjs')

# Subscribe to the default topic from the default broker
sub()
# Publish payload to topic
pub('helifgjs')

# User can pub a message to ask this to pub a message about the current state

def parse_payload(payload="kgh"):
	# Split the payload into their differet key value pairs
	properties = payload.split(';')
	# Loop through each key value pair
	for prop in properties:
		prop = prop.split('=')

def set_stuff(prop):
	# Get the key value pair out of the list
	key = prop[0]
	val = prop[1]
	# If the key is a valid key

from pi_controller import getAirconController

ac = getAirconController()

def set_state(set_this, to_this):
	if set_this == None or to_this == None:
		return False
	elif set_this == 'mode':
		if to_this == 'auto':
			ac.on()