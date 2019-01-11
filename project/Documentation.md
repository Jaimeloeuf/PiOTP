You can only control the aircon by using the same reference to the one ac controller created at the start of the program.
All modules who import it has access and the ability to control it.

### Control / main modules and functions
- main.py :
	This module contains the Flask server

### Utilities libraries and modules
- MQTT module:
	A simple wrapper library/module over the single ended pub and sub actions provided by the paho MQTT package.
- pi_controller module:
	Defines the AC controller and its methods, for us to set AC state.
- BME_control module:
	Module used to read values (temp, humidity) from the BME Sensor.