You can only control the aircon by using the same reference to the one ac controller created at the start of the program. All modules who import it has access and the ability to control it.

### Main modules and their functions
- pi_controller module:
	This module is the 'glue' code that acts as the main control software on the Pi.
	It will act as the intermediary code on the Pi between the BME sensor controller,
	the AC controller and the MQTT Client connections to the broker.
- Server package:
	This module contains the Flask server, that is 'physical server' agnostic, and can run both
	on the Pi as a seperate process, or on an external VPS.

### Utilities libraries and modules
- JQTT package:
	A simple wrapper library/module over the single ended pub and sub actions provided by the paho MQTT package.
- Jevents package:
	A simple Events and Data observer library.
- JSutils package:
	A simple library that implements certain native JS features such as setInterval.
- ac module:
	Defines and exposes the AC controller object and its methods, for us to set AC state.
- BME module:
	Module used to read values (temp, humidity) from the BME Sensor.


#### LEGEND:
- rp: raspberry pi
- ac: aircon
- bz: buzzer
- btn: button

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


### Topics used in the Broker
The topic names are created by its unique name plus the prefix infront of it.
	prefix = 'IOTP/grp4/channel/'

- Command and Action topic is:
	prefix + 'cact'
	Publishers of this topic:
		- Client application (either native or web)
		- Web Service ??
	Consumer of this topic:
		- MQTT client on the Pi subscribes to this data and relays it to the AC controller after authentication

- Sensor data topic is:
	prefix + 'sdat'
	Publishers of this topic:
		- (BME Sensor reader -> Pi -> MQTT Client library) The MQTT client on the Pi publishes data from the sensor reader module
	Consumer of this topic:
		- Web service (for data visualisation)
		- Client application (either native or web)




The reading of data from the sensor is independant of the current mode. A setInterval loop will call the function repeatedly to update the variable. Everytime the variable updates, event handlers or callbackfunctions will be called.
A global variable will maintain 'state'/record of the current operating mode.
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



Everytime AC state changes, the pi_controller will publish by MQTT to the 'ac_state' topic.




====================================================================================================================================
	List of possible valid messages that will be received from the MQTT broker

Should I make all of the incoming messages url encoded? So I can just use any library or smth to parse
	it for me instead of writing my own parser and switcher function.
	Turn all of this into regex to search for incoming messages if not using the urlencoded method
should there be different parsers based on which mode is currently operating?

	ac=on;
		Turn the AC on regardless of current state.
		When this command is received and the Pi is in the auto/timed mode
			change the mode to manual
			and turn ac on

	ac=on;time=x;
		Where x is the time that the AC will be on for.
		Use ac'=off;' message to off the AC manually

	ac=off;
		When this command is received and the Pi is in the auto/timed mode
			change the mode to manual
			and turn ac off

	mode=man;
		Do not change the current state of the AC
		Just change the mode to man, and disable all the auto controls to the AC

	mode=auto;
		Do not change the current state of the AC
		Just change the mode to auto, and set the callbacks and everything and let it run

	mode=timed;
		!!! Timed mode means, on for a set time, or on for a specific time of the day.
		In the timed mode, another message will be expected

timed mode's actions can be interrupted by incoming messages that changes mode or ac state directly.
In timed mode, the pi_controller will constantly wait for 2 different timed mode specific commands, to set a timeout value or a timeZone?

	time=x;
		Turn the AC on regardless of current state.
		Create a timer to countdown with the given time to off the AC after that, if at anypoint, the
		ac is offed, or this mode is 'turned off' then kill the timer

	start=x;end=y;repeat=true;?
		Disable everything and just wait for the start time, --> use a event thing or smth for the start time
		when it is start time, on the AC and wait for the end time
		when it is the end time, off the AC and put the system into timed mode.       doing nth and waiting for a new time?
		The last kv pair received is optional and is used to indicate if the timed mode should constantly operate at the set time over and
		over again through multiple days, if false or unset, then it will nvr repeat.


mode is basically choosing which "pi controller" to use to control the pi's ac
^ Somewhat true



=============================================================================
#### Misc Info:
On using JavaScript in python directly using JS eval packages:
- These can be used to implement the functions that I rewrote in native Python in the JSutils library, but did not due to the need of including additional dependencies and bloat.
	- [PyMiniRacer](https://github.com/sqreen/PyMiniRacer)
	- [Js2Py](https://pypi.org/project/Js2Py/)
	


Define all the global variable and functions first. Then at the bottom have a main function that uses them in one go... This means that I can import functions from outside modules