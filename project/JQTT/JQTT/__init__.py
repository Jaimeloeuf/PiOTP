""" Dependencies """
from .mqtt import set_broker, set_topic
from .pub import pub
from .sub import sub

if __name__ == "__main__":
	# If module called as standalone module, run the example code below to demonstrate this MQTT client lib
	set_topic("JJ_topic", 'p') # Set publisher topic
	pub('helifgjs') # Publish payload to topic
	sub() # Subscribe to the default topic from the default broker
	pub('helifgjs') # Publish payload to topic