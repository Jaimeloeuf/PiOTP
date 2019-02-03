""" 
Module Desciption:
    This module is the code that will be running on the Pi to glue together the operations
    of the MQTT Client lib, the AC controller and the BME sensor interface.
    User can pub a message to ask the pi_controller to pub a message about the current state.
"""

# MQTT Client library
from JQTT import pub, sub, set_broker, set_topic, Publisher
# Get the AC controller from the ac module.
from ac import ac
# A data Watcher using the observer pattern
# from Jevents import Watch
from Jevents import Watch, wait_for_daemons
# from BME import bme as BME
# Import the setInterval class from JSutils package
from JSutils import setInterval


""" Global Variables: """
# Create a new global variable to store sensorData with a initial state of None using the Watch class.
sensorData = Watch(None)
# Create a new global variable to store interval time between calls to update the sensor data.
intervalTime = Watch(30)  # Initial value of 30 seconds intervals

# Create a Publisher object for sensor data. Set the publish topic to 'SenD' meaning 'sensor data'
SensorData_Publisher = Publisher('IOTP/grp4/channel/SenD', on_connect=True, on_publish=True)
# Create a Publisher object for Interval Time. Set the publish topic to 'IntT' meaning 'Interval Time'
IntervalTime_Publisher = Publisher('IOTP/grp4/channel/IntT', on_connect=True, on_publish=True)

# Function used to publish the new time.  -->  USe a decorator instead.
def func():
    IntervalTime_Publisher.pub(f'Interval time successfully updated to: {intervalTime.value}')
# Everytime the interval time is successfully updated, the Pi will produce and publish a new Event.
intervalTime.on_set(func) # Make this into a decorator of some sort to use the above function

# Function used to restart the interval loop
def restart_loop():
    # Allow referencing of the global variable. Do I need this? Since only method calls are used on the object
    global intervalTimerRef
    # Stop the old interval
    intervalTimerRef.stop()
    # Start a new interval loop and assign it to the same variable
    intervalTimerRef = setInterval(intervalTime.value, readData)
    IntervalTime_Publisher.pub('Interval Loop has been successfully restarted')
# Everytime the interval time is successfully updated, Pi_controller needs to restart the loop
intervalTime.on_set(restart_loop) # Make this into a decorator of some sort to use the above function


# Function called every "interval" to update sensorData and publish it to the Broker
def readData():
    # Reference the variable in the global file scope, do I need this? Since I am only calling a method on the object
    global sensorData
    # Read data from sensor and store inside the sensorData object
    sensorData.set(BME.getData())
    # Publish the data to with the pre-defined Publisher
    SensorData_Publisher.pub(sensorData.value)


# Call the readData function every "intervalTime" to update the sensor Data and store the reference to this loop in a global variable
intervalTimerRef = setInterval(intervalTime.value, readData)


# Function to change interval time variable. Interval span can be changed by the User via MQTT
def setIntervalTime(time):
    # Function will be ran on message received.
    intervalTime.set(time)



# The below will be set by the different modes. On setting a new mode, do this
# Every time there is a new data,

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
    if sensorData.value > threshold and ac.state() == 'off':
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




# Call the wait function to stop main thread from ending before the daemonic threads finnish
wait_for_daemons() # Blocking call at the end of the main thread execution.