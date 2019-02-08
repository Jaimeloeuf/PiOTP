""" 
Module Desciption:
    This module is the code that will be running on the Pi to glue together the operations
    of the MQTT Client lib, the AC controller and the BME sensor interface.
    User can pub a message to ask the pi_controller to pub a message about the current state.

    Diff between pi controller 1 and 2 is that 2 does not have a timed mode.
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
# Create a Publisher object for Events on the Pi.
Event = Publisher('IOTP/grp4/channel/events', on_connect=True, on_publish=True)
# Create a Publisher object for all the Error Events and its messages
ErrorPublisher = Publisher('IOTP/grp4/channel/error', on_connect=True)
# Make a Subscription to the Command topic with the Default handler for the on_connect event used
command_pipe = Subscription('IOTP/grp4/channel/cmnd', on_connect=True)



# Callback function that runs the operating mode initialization functions when mode changes
def change_mode(mode):
    if mode == 'auto':
        mode_auto()
    elif mode == 'man':
        mode_man()
    else:
        # Create the error message
        Err_Msg = f"Invalid mode is being passed: {mode}"
        # Publish the error message
        ErrorPublisher < Err_Msg
        # Print/Log error
        print(Err_Msg)
        # Return false to indicate error and operation failure
        return False
    # If there was no error, publish this change of mode as an event
    Event < f"Mode: {mode}"
    # Return True to indicate operation success
    return True


# Callback function that runs when command received from command pipeline is 'ac'
def ac_state(state):
    if state == 'on':
        ac.on()
    elif state == 'off':
        ac.off()
    else:
        # Print/Log error
        print('Invalid AC state received')
        # Return false to indicate error and operation failure
        return False
    # Return True to indicate operation success
    return True


# Callback function to change interval time variable when command is intervalTime
def setIntervalTime(time):
    # Set the interval time and let the callback functions deal with the rest
    intervalTime < time
    # Return True to indicate operation success
    return True


# Dictionary that holds all the functions for the given commands
dispatch = {
    "mode": change_mode,
    "ac": ac_state,
    "intervalTime": setIntervalTime
}


# Callback function used to parse messages/payload from the MQTT broker
def parseMsg(msg):
    # msg are concatenations of kv pair(s)
    # Seperate the kv pairs first
    kv_pairs = msg.split(';')

    # Inner function for cleaning and formatting strings
    def clean_string(str):
        # Strip all the white spaces
        if isinstance(str, list):
            for index, item in enumerate(str):
                str[index] = item.strip()
            return str
        else:
            return str.strip()

    # Clean and format the input
    kv_pairs = clean_string(kv_pairs)
    
    # Loop through all the key value pairs
    for kv in kv_pairs:
        # Unpack the output from splitting the string as command and its arguements
        command, args = kv.split(':')

        # # Check if key exists in the dictionary first
        # if command in dispatch:
        #     # Run the command function with the args and check for its return statement
        #     if not dispatch[command](args):
        #         # If the operation failed
        #         # Create the error message
        #         Err_Msg = f"Invalid command received from MQTT Broker: {command} + {args}"
        #         # Publish the error to the error topic
        #         ErrorPublisher < Err_Msg
        #         # Print/Log error
        #         print(Err_Msg)
        #         # Return false to indicate error and operation failure
        #         return False
        # else:
        #     # Key is not a valid command
        #     # Create the error message
        #     Err_Msg = f"Invalid command received from MQTT Broker: {command} + {args}"
        #     # Publish the error to the error topic
        #     ErrorPublisher < Err_Msg
        #     # Print/Log error
        #     print(Err_Msg)
        #     # Return false to indicate error and operation failure
        #     return False

        # Check if key exists in the dictionary first
            # Run the command function with the args and check for its return statement
        if (command in dispatch) and dispatch[command](args):
                pass
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


def publish_int_time_change():
    Event < f'Interval time updated to: {intervalTime}'
publish_int_time_change = lambda data: Event < f'Interval time successfully updated to: {data}'

# Function used to restart the interval loop
def restart_loop():
    # Allow referencing of the global variable. Do I need this? Since only method calls are used on the object
    global intervalTimerRef
    # Stop the old interval
    intervalTimerRef.stop()
    # Start a new interval loop and assign it to the same variable
    intervalTimerRef = setInterval(intervalTime, readData)
    Event < 'Interval Loop restarted'

# Function called every "interval" to update sensorData and publish it to the Broker
def readData():
    # Reference the variable in the global file scope, do I need this? Since I am only calling a method on the object
    global sensorData
    # Read data from sensor and store inside the sensorData object
    sensorData(BME.getData())
    # Publish the data to with the pre-defined Publisher
    SensorData_Publisher < sensorData


""" The below functions are to run as "init" functions when the modes are first set.
    They will clear all callback functions and attach new ones for that particular mode.
"""
# Init function for the auto operating mode
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

# Init function for the manual operating mode
def mode_man():
    """ Initialization function for the manual operating mode """
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.clearAllListeners()
    # No callbacks needed as manual mode just waits for input from the MQTT Broker or the Btn



# This is the program's entry point. In last block to make sure all funcs and vars are defined prior to use
if __name__ == "__main__":
    """ Attach all the callback functions defined above to their
        respective Events and just wait for the Events to happen.
    """
    # When the mode is changed, call the init switcher function.
    operating_mode.on_change += change_mode

    # Everytime the interval time is set, the Pi will produce and publish a new Event.
    intervalTime.on_set += restart_loop
    # Everytime the interval times
    intervalTime.on_change += publish_int_time_change

    """ Test code """
    parseMsg('mode:man; ac:on')


    # Attach the parseMsg function as the callback handler for on_message events from the command pipeline
    command_pipe.on_message += parseMsg

    # Start the manual mode as the initial default mode, by setting the mode to 'man'
    operating_mode < 'man'

    # Start the loop to call readData function every "intervalTime" to update sensor Data on the global loop reference
    intervalTimerRef = setInterval(intervalTime.value, readData)

    # Do nothing, pause and wait for events to happen.
    # Call the wait function to stop main thread from ending before the daemonic threads finnish
    wait_for_daemons() # Blocking call at the end of the main thread execution.