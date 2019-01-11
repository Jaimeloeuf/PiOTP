from paho.mqtt.client import Client

# Global variable that stores the topic name
topic = "tp/eng/iotp/jj"


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def onMsg(payload):
    print(payload)
    if payload == 'mode: auto':
        pass
    if payload == 'mode: com':
        pass
    if payload == 'mode: man':
        pass
    if payload == 'mode: off':
        pass
    if payload == 'ac: on':
        pass
    if payload == 'ac: off':
        pass


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# Create a new MQTT client
# If you want to use a specific client id, use mqttc = mqtt.Client("client-id")
# note that the client id must be unique on the broker
mqttc = Client()
# print("\nCreated client object at " + time.strftime("%H:%M:%S"))
# Set all the event handlers and call backs
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Connect to the broker and start the network loop
mqttc.connect("m2m.eclipse.org")
mqttc.loop_start()

payload = "gsus"
# Publish the payload and wait for it to be published


def pub(payload):
    mqttc.publish(topic, payload, qos=2).wait_for_publish()


pub(payload)
