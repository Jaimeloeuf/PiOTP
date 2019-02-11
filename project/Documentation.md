### Main modules and their functions
- pi_controller module:
	This module is the 'glue' code that acts as the main control software on the Pi.
	It will act as the intermediary code on the Pi between the BME sensor controller,
	the AC controller and the MQTT Client connections to the broker.
- Server package:
	This module contains the Flask server, that is 'physical server' agnostic, and can run both
	on the Pi as a seperate process, or on an external VPS.


### Utilities libraries, external dependencies and modules
- [JQTT package](https://github.com/Jaimeloeuf/JQTT):
	A simple wrapper library/module that provides a Publisher and Subscription module that can extends on the Client Class of the paho-mqtt package and also 2 wrapped single pub and sub actions functions.
- [Jevents package](https://github.com/Jaimeloeuf/Jevents):
	A simple Events and Data observer library used to implement data on change callback calling behaviours.
- [JSutils package](https://github.com/Jaimeloeuf/JSutils):
	A simple library used to emulate the setInterval native JavaScript feature.
- ac module:
	Defines and exposes the AC controller object and its methods, for us to set AC state.
- bme module:
	Module used to read values (temp, humidity) from the BME Sensor.


#### LEGEND:
- rp: raspberry pi
- ac: aircon
- bz: buzzer
- btn: button


#### So what is the use case scenario?
1.	Manual mode
    - Mode that allows user to manually control the AC module using either
		- A Command from the MQTT broker
		- Physical push button

2.	Auto mode
    - Constantly monitor the temp and cool hse if needed
        - The device reads temp on every interval
        - if the temperature is too high
			- On ac
        - Temp not too high
			- off ac if it was on.
    - Features currently being worked on:
		- Set a "timezone" thing, so that the auto mode is only activated when it is in the current time now.
		- Set a "I'm coming home" mode. So just click on this mode before coming home, it will start the auto mode automatically

3.	Timed mode
	- On the AC for a set amount of time.
	- The mode is ran using the command from the MQTT Broker.
	- Operating mode will change back to manual mode when the AC turns off


### Topics used in the Broker
The topic names are created by its unique name plus the prefix infront of it.
	prefix = 'IOTP/grp4/channel/'

- Command and Control topic is:
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


### How the Pi Controller works
- Sensor data will be read repeatedly at a fixed interval independant of the current operating mode.
- A setInterval loop will call the function repeatedly to update the sensor data variable, and everytime the variable updates, event handlers or callbackfunctions will be ran.
- A global variable will maintain 'state'/record of the current operating mode.
- A global variable stores the sensor data which is being 'Watched' to run event handlers
- The pi_controller will publish the state of the AC everytime it changes.
- All the function and global variables are defined and declared in the Pi Controller before they are used in the 'main' function of the module which lives in the 'if' block that checks if module ran as 'main'.
- The aircon can only be controlled using the same reference to the one ac controller object created at the start of the program. No more than one ac object should be created from the acController class. All modules who import it has access and the ability to control it, but should not change its reference to prevent problems in other modules/packages.

#### The different modes of the Pi Controller
Since data is always read at the given interval, the init functions of the modes' just attach event handlers or callback functions to run when the variable is updated.

- Manual mode:
	- Do nth but publish the data and wait for incoming commands from the MQTT broker
	--> repeat

- Auto mode:
	- On every sensor data update, check if the sensor data exceeded the threshold variables
		if exceeded
			change AC state, should there be an on time given? to off the AC after a specified time
			publish above event to broker
		elif below threshold but AC still on:
			off AC
			publish abv event to broker
	--> repeat

- Timed mode:
	- Do nth but publish the data and wait for incoming commands from the MQTT broker
	--> repeat
	(in the background):
	Timer object running, where the AC is set to on, with a timeout using the timer object to off it.

### List of possible valid messages that will be received from the MQTT broker
- ac=on;
	Turn the AC on regardless of current state.
	When this command is received and the Pi is in the auto/timed mode
		change the mode to manual
		and turn ac on

- ac=on;time=x;
	Where x is the time that the AC will be on for.
	Use ac'=off;' message to off the AC manually

- ac=off;
	When this command is received and the Pi is in the auto/timed mode
		change the mode to manual
		and turn ac off

- mode=man;
	Do not change the current state of the AC
	Just change the mode to man, and disable all the auto controls to the AC

- mode=auto;
	Do not change the current state of the AC
	Just change the mode to auto, and set the callbacks and everything and let it run

- mode=timed;
	!!! Timed mode means, on for a set time, or on for a specific time of the day.
	In the timed mode, another message will be expected

timed mode's actions can be interrupted by incoming messages that changes mode or ac state directly.
In timed mode, the pi_controller will constantly wait for 2 different timed mode specific commands, to set a timeout value or a timeZone?

- time=x;
	Turn the AC on regardless of current state.
	Create a timer to countdown with the given time to off the AC after that, if at anypoint, the
	ac is offed, or this mode is 'turned off' then kill the timer

- start=x;end=y;repeat=true;?
	Disable everything and just wait for the start time, --> use a event thing or smth for the start time
	when it is start time, on the AC and wait for the end time
	when it is the end time, off the AC and put the system into timed mode.       doing nth and waiting for a new time?
	The last kv pair received is optional and is used to indicate if the timed mode should constantly operate at the set time over and
	over again through multiple days, if false or unset, then it will nvr repeat.


#### Misc Info:
On using JavaScript in python directly using JS eval packages:
- These can be used to implement the functions that I rewrote in native Python in the JSutils library, but did not due to the need of including additional dependencies and bloat.
	- [PyMiniRacer](https://github.com/sqreen/PyMiniRacer)
	- [Js2Py](https://pypi.org/project/Js2Py/)