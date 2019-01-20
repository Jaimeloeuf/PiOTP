""" Dependencies """
from JQTT.mqtt import get_broker, get_topic, set_broker, set_topic
from JQTT.pub import pub
from JQTT.sub import sub

if __name__ == "__main__":
	# If module called as standalone module, run the example code below to demonstrate this MQTT client lib
	set_topic("my_topic", 'p') # Set publisher topic
	pub('helifgjs') # Publish payload to topic

	set_topic("my_topic", 's') # Set publisher topic
	print('topic for s after setting is: ', get_topic('s'))
	from JQTT.sub import topic
	print('topic for s after setting is: ', topic)

	def hi(a, b, c):
		print(a, b, c)
	sub(hi) # Subscribe to the default topic from the default broker

	pub('helifgjs') # Publish payload to topic
	print('published')