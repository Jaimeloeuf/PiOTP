import time
import paho.mqtt.client as mqtt

broker = "m2m.eclipse.org"
port = 1833
topic = "tp/eng/iotp_lab/pc_01"


def create_client():
	return mqtt.Client()

def connect(client, broker, port=1833)
    client.connect(mqtt_broker, port)
    print("--connected to broker")


def publish(client, topic, msg):
	try:
        client.publish(topic, msg)
    except:
        print("--error publishing!")
		return Error
    else:
        client.disconnect()
        print("--disconnected from broker")

def onMsg(msg):
	print(msg)

def sub(client, broker, topic, qos=2, port=1833):
	client.on_message = onMsg




client = create_client()
print("\nCreated client object at " + time.strftime("%H:%M:%S"))
connect(client, broker, port)
msg = "Hi"
publish(client, topic, msg)