You can only control the aircon by using the same reference to the one ac controller created at the start of the program.
All modules who import it has access and the ability to control it.

### Control / main modules and functions
- Server module:
	This module contains the Flask server, that is 'physical server' agnostic, and can run both on the Pi
	as a seperate process, or on an external VPS.
- pi_controller module:
	This module is the 'glue' code that acts as the main control software on the Pi.
	It will act as the intermediary code on the Pi between the BME sensor controller, the AC controller and
	the MQTT Client connections to the broker.

### Utilities libraries and modules
- MQTT module:
	A simple wrapper library/module over the single ended pub and sub actions provided by the paho MQTT package.
- ac module:
	Defines and exposes the AC controller object and its methods, for us to set AC state.
- BME module:
	Module used to read values (temp, humidity) from the BME Sensor.


#### LEGEND:
- rp: raspberry pi
- ac: aircon
- bz: buzzer

#### So what is the use case scenario?
1. Manual mode (Use phone to turn on and off the air con remotely)
    - Rmb that this means that I would need to control the rasp pi remotely.
    - Use MQTT without any security for now.
        - The "server" on the pi subscribes to the MQTT broker's topic,
        - Listens to commands that will come in.

2. Auto mode
    1. Set a "I'm coming home" mode. So just click on this mode before coming home, it will check temp and cool if needed
    2. "Always auto mode" that will constantly monitor the temp and cool hse if needed
        - This method means that the rp will be checking the temp every few seconds or mins
        - ?	determine if the temperature is too high
        - On ac
        - : off ac if it was on.
    3. Set a "timezone" thing, so that the auto mode is only activated when it is in the current time now.


### Topics used in the Broker, and also the default Topics inside the MQTT library

The topic names are created by its unique name plus the prefix infront of it.
	prefix = 'IOTP/grp4/channel/'

Command and Action topic is:
- prefix + 'cact'
Publishers of this topic:
- Client application (either native or web)
- Web Service ??
Consumer of this topic:
- MQTT client on the Pi subscribes to this data and relays it to the AC controller after authentication

Sensor data topic is:
- prefix + 'sdat'
Publishers of this topic:
- (BME Sensor reader -> Pi -> MQTT Client library) The MQTT client on the Pi publishes data from the sensor reader module
Consumer of this topic:
- Web service (for data visualisation)
- Client application (either native or web)

















Every message received in the Topic: 'command+actions' should be a kv pair thing
So the key is the command, and the value is the action or the value or the thing...
E.g.

key is the thing to act upon
value is the action or state that should be applied to the key

ac=on
ac=off
set_sd_interval= # Can set the interval in which the sensor data will be read.
^ Abv commands can be sent regardless of what mode it is now operating in.

The reading of data from the sensor is independant of the current mode. A setInterval loop will call the
function over and over again to update the variable. Everytime the variable updates, there can be event handlers.

The event handlers should be called every single time the set method of the object is called.

Should I get the event handlers to run in another thread?
Also should the MQTT work in another background thread?

	So based on the global variable, decide what mode it is operating in,
	choose a function for that mode, and apply that as a cb to the addlistener for the sensoor data
	when the variable itself is updated, use a event and callback to change the callback function of the sensor data
	To set a new cb function, use a method to either clear all listeners or remove last listener on the stack,
	before setting the new cb into it.
	

	Make everything into data that is watched so everything will be like node js events
	- Like the brokers and the topics should also be watched so when anything changes, there
	can be event handlers, so you no longer need to set the publisher and broker every single time before publishing data
	when the sensordata changes.

The different modes
	Data is always read at the given interval and the value is always updated after reading.
	The function for all these modes will just be event handlers that will be called when the value is updated

		sub to the broker's 'man' cmd topic,
		given a new msg that the broker pushed down, do what is requested for
			If the state of the AC is changed, publish the event too.


Man:
	# Do nth but publish the data, the pi_controller should not control the ac directly, only the incoming msg can
	publish the sensor data to the broker
	--> repeat

Auto:
	publish the sensor data to the broker
	Check if the sensor data exceeded the threshold variables
		if exceeded
			change AC state, should there be an on time given? to off the AC after a specified time
			publish above event to broker
		elif below threshold but AC still on:
			off AC
			publish abv event to broker
	--> repeat

Timezone:
	publish the sensor data to the broker
	--> repeat

	(in the background):
	Timer object running, cos the AC is set to on, but with a timeout to off it.


	Implement the watch var class to the AC controller.


