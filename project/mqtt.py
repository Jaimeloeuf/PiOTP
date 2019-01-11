""" Dependencies """
from pub import pub, set_broker as set_pub_broker, set_topic as set_pub_topic
from sub import sub, set_broker as set_sub_broker, set_topic as set_sub_topic

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
