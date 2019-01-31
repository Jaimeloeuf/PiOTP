""" 
Module Desciption:
    This module is the code that will be running on the Pi to glue together the operations
    of the MQTT Client lib, the AC controller and the BME sensor interface.
    User can pub a message to ask the pi_controller to pub a message about the current state.
"""

# Dependencies
# MQTT Client lib
# from mqtt import pub, sub, set_broker, set_topic
from JQTT import pub, sub, set_broker, set_topic
# Get the AC controller from the ac module.
from ac import ac
from data_watcher import watch
# from BME import bme as BME
# Import the setInterval class from JSutils package
from JSutils import setInterval

""" Global Variables: """
# Create a new global variable to store sensorData with a initial state of None using the watch class.
sensorData = watch(None)
# Create a new global variable to store interval time between calls to update the sensor data.
intervalTime = watch(30)  # Initial value of 30 seconds intervals

# Function used to publish the new time.  -->  USe a decorator instead.
def func():
    set_topic('new interval time', 'p')
    pub(intervalTime.get())

# Everytime the interval time is successfully updated, the Pi will produce and publish a new Event.
intervalTime.addListener(func)

# Function that will be called every "interval" to update the sensorData and publish the the data to the Broker
def readData():
    # Reference the variable in the global file scope
    global sensorData
    # Read data from sensor and store inside the sensorData object
    sensorData.set(BME.getData())
    # Set the publish topic to 'send', or 'sensor data'
    set_topic('send', 'p')
    # Publish the data to the MQTT Broker
    pub(sensorData.get())


# Call the readData function every "intervalTime" to update the sensor Data and store the reference to this loop in a global variable
intervalTimerRef = setInterval(intervalTime.get(), readData)
intervalTimerRef.stop()  # Stop the interval loop

# Function to change interval time variable. Interval span can be changed by the User via MQTT
def setIntervalTime(time):
    intervalTime.set(time)

    # Allow referencing of the global variable
    global intervalTimerRef
    # Stop the old interval
    intervalTimerRef.stop()
    # Start a new interval loop and assign it to the same variable
    intervalTimerRef = setInterval(intervalTime.get(), readData)

    """ TO move this code and the interval time var down below the interval timer ref as python no var hoisting. """
    """ To implement feature in the ac module to auto pub state change every time. """

    # Publish the message with the newly set intervalTime after everything is done.
    pub(f'Interval time successfully updated to: {intervalTime.get()}')


# There can only be one timerLoop that calls the readData function in the whole running process to prevent data duplication
# Is there hoisting in python code?


# Set topic to subscribe to.
# set_topic("cact", 's')
# Subscribe to the topic that has been set.
# sub(parse_payload)


# The below will be set by the different modes. On setting a new mode, do this
# Every time there is a new data,
# sensorData.addListener()


# Function that returns the different functions to run as eventListeners/background-task when a new mode is used
# Every time the mode changes, execute/call the init function of that mode.
def change_mode(mode):
    if mode == 'auto':
        return mode_auto
    elif mode == 'man':
        return mode_man
    elif mode == 'timed':
        return mode_timed
    else:
        # Print/Log error
        print('Invalid mode is being passed')
        return False  # Return false to indicate error and operation failure


# GLobal variable to keep track of the threshold value of the highest temperature.
threshold = None

# Callback function that runs everytime the sensorData variable is updated and the pi is currently running on auto mode.
# Function checks variable against the threshold and change state of AC if needed.
def auto_cb():
    global threshold
    global ac
    # On the AC if temp exceeds threshold and it is off.
    if sensorData.temp > threshold and ac.state() == 'off':
        ac.on()
    # Off the AC if temp does not exceed threshold and it is on.
    elif ac.state() == 'on':
        ac.off()


# The below functions are to run as "init" functions when the modes are first set.
# All they do is clear all the event handlers and attach new handlers for that particular mode.

def mode_auto(state):
    # If this is the current running mode, just wait for new incoming commandss
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.removeListener()
    # At every interval, the variable is updated and the data is published to the MQTT broker, thus I do not need to publish it again.
    # The callback passed in to it runs every time the variable is updated whilst in auto mode.
    sensorData.addListener(auto_cb)

    # Should the data_watcher class pass the value of the data to the callback functions too?

    # Below function is called on new command/msg. Function to return this inner function
    def onMessage(msg):
        pass
        # Parse the message to determine what it is trying to say
        # Verify that it is a valid message.
                    # If valid then do it
                    # else reject the message by publishing a 400 bad request?

        # Make the below into a generator function that I can constantly yield new values out of.
        # The yeild is to pause the execution of the function upon the so called "wait"

def mode_man():
    # If this is the current running mode, just wait for new incoming commandss
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.removeListener()
    # Since at every interval, the variable is updated and the data is published to the MQTT broker, there is no need to do any other thing but wait for commands from MQTT that requests for a ac state change

    # Below function is called on new command/msg. Function to return this inner function
    def onMessage(msg):
        pass
        # Parse the message to determine what it is trying to say
        # Verify that it is a valid message.
            # If valid then do it
            # else reject the message by publishing a 400 bad request?


def mode_timed():
    # If this is the current running mode, just wait for new incoming commands
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.removeListener()
    # For the timed mode, listen for this few messages
    # AC state change command
    # Mode change command
    # Set new time period/new timeout
