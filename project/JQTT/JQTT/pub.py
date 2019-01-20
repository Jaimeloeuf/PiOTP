""" Dependencies """
import paho.mqtt.publish as publish

# This is the prefix for all the topics.
topic_prefix = "IOTP/grp4/channel/"
# Global variable to store the topic name, default topic is here too
topic = ""
# Global variable to store the topic name, default topic is here too
broker = "m2m.eclipse.org"


def set_broker(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global broker
    broker = data


def set_topic(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global topic
    # Create the topic by prepending the prefix to the received data and saving inside the global topic variable
    topic = topic_prefix + data
    # Return topic for the function caller to use if needed.
    return topic


def pub(payload):
    publish.single(topic, payload, 1, hostname=broker)
