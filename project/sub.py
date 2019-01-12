""" Dependencies """
# Client class to create MQTT Clients
from paho.mqtt.client import Client
import paho.mqtt.subscribe as subscribe

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


def new_Msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))


# Subscribe function that subscribes to the topic and broker stored in this module.
def sub(cb):
	subscribe.callback(cb if cb else new_Msg, topic, hostname=broker)

""" Below is code to subscribe to multiple topics """
# topics = ['#']
# m = subscribe.simple(topics, hostname="iot.eclipse.org", retained=False, msg_count=2)
# for a in m:
#     print(a.topic)
#     print(a.payload)