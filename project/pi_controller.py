""" 
Module Desciption:
    This module is the code that will be running on the Pi to glue together the operations
    of the MQTT Client lib, the AC controller and the BME sensor interface.
    User can pub a message to ask the pi_controller to pub a message about the current state.
"""

# MQTT Client library
from JQTT import pub, sub, set_broker, set_topic, Publisher, Subscription
# Get the AC controller from the ac module.
from ac import ac
# A data Watcher using the observer pattern
# from Jevents import Watch
from Jevents import Watch, wait_for_daemons
# from BME import bme as BME
# Import the setInterval class from JSutils package
from JSutils import setInterval


""" Global Variables: """
# Global variable used to store the current operating state of the Pi.
operating_mode = Watch()
# Global variable used to store sensorData wrapped in a Watch Class object.
sensorData = Watch()
# Global variable used to store interval time between calls to update the sensor data.
intervalTime = Watch(30)  # Initial value of 30 seconds intervals
# Global variable holding the reference to the interval loop
intervalTimerRef = None
# GLobal variable to keep track of the threshold value of the highest temperature.
threshold = None

""" Create all the Publisher objects in the Global file scope too """
# Create a Publisher object for sensor data. Set the publish topic to 'SenD' meaning 'sensor data'
SensorData_Publisher = Publisher('IOTP/grp4/channel/SenD', on_connect=True, on_publish=True)
# Create a Publisher object for Interval Time. Set the publish topic to 'IntT' meaning 'Interval Time'
IntervalTime_Publisher = Publisher('IOTP/grp4/channel/IntT', on_connect=True, on_publish=True)
# Create a Publisher object for all the Error Events and its messages
ErrorPublisher = Publisher('IOTP/grp4/channel/error', on_connect=True)
# Make a Subscription to the Command topic with the Default handler for the on_connect event used
command_pipe = Subscription('IOTP/grp4/channel/cmnd', on_connect=True)







""" Every time the mode changes with, execute/call the init function of that mode. """
# Callback function that runs when operating mode changes
def change_mode(mode):
    if mode == 'auto':
        return mode_auto()
    elif mode == 'man':
        return mode_man()
    elif mode == 'timed':
        return mode_timed()
    else:
        # Create the error message
        Err_Msg = f"Invalid mode is being passed: {mode}"
        # Publish the error message
        ErrorPublisher < Err_Msg
        # Print/Log error
        print(Err_Msg)
        # Return false to indicate error and operation failure
        return False

# Command function that runs when command received from command pipeline is 'ac'
def ac_state(state):
    if state == 'on':
        return ac.on()
    elif state == 'off':
        return ac.off()
    elif state == 'on x':
        # Where x is the time to be on for
        return ac.on(x)
    else:
        # Print/Log error
        print('Invalid AC state received')
        # Return false to indicate error and operation failure
        return False


# Function to change interval time variable. Interval span can be changed by the User via MQTT
def setIntervalTime(time):
    # Function will be ran on message received.
    intervalTime.set(time)


# Dictionary that holds all the functions for the given commands
dispatch = {
    "mode": change_mode,
    "ac": ac_state,
    "interval time": setIntervalTime
    # "time": 
}


# Function used to do a basic clean on strings for further processing
def clean_string(str):
    # Strip all the white spaces
    if isinstance(str, list):
        for index, item in enumerate(str):
            str[index] = item.strip()
        return str
    else:
        return str.strip()


def parseMsg(msg):
    # msg are concatenations of kv pair(s)
    # Seperate the kv pairs first
    kv_pairs = msg.split(';')
    # Clean and format the input
    kv_pairs = clean_string(kv_pairs)
    
    # Loop through all the key value pairs
    for kv in kv_pairs:
        # Unpack the output from splitting the string as command and its arguements
        command, args = kv.split(':')

        # Check if key exists in the dictionary first
        if command in dispatch:
            # Either return it or respond to it.
            return dispatch[command](args)

            # If the operation is a success
            
            pub(f"Invalid command received from MQTT Broker: {command} + {args}")
        else:
            # Key is not a valid command
            # Create the error message
            Err_Msg = f"Invalid command received from MQTT Broker: {command} + {args}"
            # Publish the error to the error topic
            ErrorPublisher < Err_Msg
            # Print/Log error
            print(Err_Msg)
            # Return false to indicate error and operation failure
            return False


parseMsg('mode:man; ac:on')














# Function used to publish the new time.  -->  USe a decorator instead.
def publish_int_time_change():
    IntervalTime_Publisher < f'Interval time successfully updated to: {intervalTime.value}'

publish_int_time_change = lambda data: IntervalTime_Publisher < f'Interval time successfully updated to: {data}'

# Function used to restart the interval loop
def restart_loop():
    # Allow referencing of the global variable. Do I need this? Since only method calls are used on the object
    global intervalTimerRef
    # Stop the old interval
    intervalTimerRef.stop()
    # Start a new interval loop and assign it to the same variable
    intervalTimerRef = setInterval(intervalTime.value, readData)
    IntervalTime_Publisher < 'Interval Loop has been successfully restarted'



# Function called every "interval" to update sensorData and publish it to the Broker
def readData():
    # Reference the variable in the global file scope, do I need this? Since I am only calling a method on the object
    global sensorData
    # Read data from sensor and store inside the sensorData object
    sensorData(BME.getData())
    # Publish the data to with the pre-defined Publisher
    SensorData_Publisher < sensorData

# Look at the below module to see how to use
import json


""" The below functions are to run as "init" functions when the modes are first set.
    They will clear all callback functions and attach new ones for that particular mode.
"""
def mode_auto():
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.clearAllListeners()

    # Callback function to check variable against threshold and change state of AC if needed
    def threshold_check(data):
        global ac
        # On the AC if temp exceeds threshold and it is off.
        if sensorData > threshold:
            if ac == 'off':
                ac.on()
        # Off the AC if temp does not exceed threshold and it is on.
        elif ac == 'on':
            ac.off()

    # The callback passed in to it runs every time the variable is changed whilst in auto mode.
    sensorData.on_change += threshold_check

    # Below function is called on new command/msg. Function to return this inner function
    def onMessage(msg):
        pass
        # Parse the message to determine what it is trying to say
        # Verify that it is a valid message.
        # If valid then do it
        # else reject the message by publishing a 400 bad request?

        # Make the below into a generator function that I can constantly yield new values out of.
        # The yeild is to pause the execution of the function upon the so called "wait"
    # Add the callback function for subscribe
    sub(onMessage)

def mode_man():
    """ Initialization function for the manual operating mode """
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.clearAllListeners()

    # Below function is called on new command/msg. Function to return this inner function
    def onMessage(msg):
        pass
        # Parse the message to determine what it is trying to say
        # Verify that it is a valid message.
        # If valid then do it
        # else reject the message by publishing a 400 bad request?


def mode_timed():
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.clearAllListeners()

    # On the ac for set amount of time.
    ac.on(x)

    # For the timed mode, listen for this few messages
    # AC state change command
    # Mode change command
    # Set new time period/new timeout


















# Only run main code if module called as the program entry point.
# Code in the last block to make sure all funcs and vars are defined prior to use.
if __name__ == "__main__":
    """ Attach callback functions defined above to the interval time variable
    
    """
    # When the mode is changed, call the init switcher function.
    operating_mode.on_change += change_mode

    # Everytime the interval time is set, the Pi will produce and publish a new Event.
    intervalTime.on_set += restart_loop

    # Attach the parseMsg function as the callback handler for on_message events from the command pipeline
    command_pipe.on_message += parseMsg
    





    # Start the manual mode as the initial default mode, by setting the mode to 'man'
    operating_mode < 'man'

    # Start the loop to call readData function every "intervalTime" to update sensor Data on the global loop reference
    intervalTimerRef = setInterval(intervalTime.value, readData)

    # Do nothing, pause and wait for events to happen.
    # Call the wait function to stop main thread from ending before the daemonic threads finnish
    wait_for_daemons() # Blocking call at the end of the main thread execution.