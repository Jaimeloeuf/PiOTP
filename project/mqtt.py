import time
import paho.mqtt.client as mqtt

mqtt_broker = "m2m.eclipse.org"
topic = "tp/eng/iotp_lab/pc_01"

while True:
    my_mqtt = mqtt.Client()
    print("\nCreated client object at " + time.strftime("%H:%M:%S"))

    my_mqtt.connect(mqtt_broker, port=1883)
    print("--connected to broker")

    try:
        my_mqtt.publish(topic, pay_load)
        print("--cpu usage percent = %.1f" % cpu_usage)
    except:
        print("--error publishing!")
    else:
        my_mqtt.disconnect()
        print("--disconnected from broker")