JQTT
--------

This package is a simplified MQTT library based on the paho MQTT library.

To publish data:
    >>> from JQTT import pub
    >>> pub('Chicken Nuggets!')


To publish data:
    >>> from JQTT import sub
	>>> def onMsg(client, userdata, message):
	>>>		print(message) # Callback function to print out the message
    >>> sub(onMsg) # Pass the function into the sub function to use it as a callback function

* For the above lib usage. The broker and topics are not set, thus the default broker and topics will be used.

To Change broker and topic:
	>>> from JQTT import pub set_broker, set_topic
	>>> set_broker('m2m.org', 'p') # Set the broker to publish to
	>>> set_topic('MQTT_test', 'p') # Set the topic to publish to
	>>> pub('Hello, test 123') # Publish the message to the abv broker's topic
