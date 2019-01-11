""" Dependencies """
import paho.mqtt.publish as publish

# Global variable to store the topic name, default topic is here too
topic = "JJ/is"
# Global variable to store the topic name, default topic is here too
broker = "m2m.eclipse.org"


def set_broker(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global broker
    broker = data


def set_topic(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global topic
    topic = data


def pub(payload):
    publish.single(topic, payload, 2, hostname=broker)
