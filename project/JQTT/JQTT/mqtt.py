""" Dependencies """
from .pub import broker as pub_broker, topic as pub_topic, set_broker as set_pub_broker, set_topic as set_pub_topic
from .sub import broker as sub_broker, topic as sub_topic, set_broker as set_sub_broker, set_topic as set_sub_topic

def set_broker(broker, pORs):
	if pORs == None:
		return False
	elif pORs == 'p':
		set_pub_broker(broker)
	elif pORs == 's':
		set_sub_broker(broker)
	else:
		return False

def set_topic(topic, pORs):
	if pORs == None:
		return False
	elif pORs == 'p':
		set_pub_topic(topic)
	elif pORs == 's':
		set_sub_topic(topic)
	else:
		return False

def get_broker(pORs):
	if pORs == None:
		return False
	elif pORs == 'p':
		return pub_broker
	elif pORs == 's':
		return sub_broker
	else:
		return False

def get_topic(pORs):
	if pORs == None:
		return False
	elif pORs == 'p':
		return pub_topic
	elif pORs == 's':
		return sub_topic
	else:
		return False
