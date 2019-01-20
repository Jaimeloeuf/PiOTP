""" Dependencies """
import paho.mqtt.subscribe as subscribe

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


def new_Msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))


# Subscribe to topic from broker in this module and use callback function provided or default new_Msg function.
def sub(cb=new_Msg):
    subscribe.callback(cb, topic, qos=1, hostname=broker)


""" Below is code to subscribe to multiple topics """
# topics = ['#']
# m = subscribe.simple(topics, hostname="iot.eclipse.org", retained=False, msg_count=2)
# for a in m:
#     print(a.topic)
#     print(a.payload)
