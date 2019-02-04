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
# Global variable used to store the current operating state of the Pi. Initially 'manual' mode
operating_mode = Watch('man')
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


def parseMsg(msg):
    # msg is a kv pair, so to check if the key exists first using a dictionary
    # Unpack the output from splitting the string
    key, value = msg.split(':')

    import MQTT_msg_parser as parser
    commands = parser.commands
    # If the key is valid
    if key in commands:
        
        # The 'value' stored for this key is another map that stores a list of possible values and their actions
        # commands.get(key).get(value)

        # Returns a function that I call with value
        commands.get(key)(value)
        commands[key](value)

        # If the operation is a success
        if commands.get(key)(value):
            pass
        else:
            pub('ERR: Invalid command action.')
    else:
        # Key is not a valid command
        # Should change all the print based debug statements into logging functions.
        print(f"Invalid command received from MQTT Broker: {key} + {value}")
        pub('ERR: Invalid command')
    

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
    SensorData_Publisher.pub(sensorData)




""" The below functions are to run as "init" functions when the modes are first set.
    They will clear all callback functions and attach new ones for that particular mode.
"""
def mode_auto(state):
    # Reference the global variable sensorData
    global sensorData
    # Remove all eventHandlers / callbacks first before adding in callbacks for this mode.
    sensorData.clearAllListeners()

    """ Definition of all the callback functions / event handlers to be used in auto mode """
    # Callback function to check variable against threshold and change state of AC if needed
    def threshold_check(data):
        global threshold
        global ac
        # On the AC if temp exceeds threshold and it is off.
        if sensorData.value > threshold and ac.state() == 'off':
            ac.on()
        # Off the AC if temp does not exceed threshold and it is on.
        elif ac.state() == 'on':
            ac.off()

    # Below function is called on new command/msg. Function to return this inner function
    def onMessage(msg):
        pass
        # Parse the message to determine what it is trying to say
        # Verify that it is a valid message.
        # If valid then do it
        # else reject the message by publishing a 400 bad request?

        # Make the below into a generator function that I can constantly yield new values out of.
        # The yeild is to pause the execution of the function upon the so called "wait"

    # The callback passed in to it runs every time the variable is set whilst in auto mode.
    sensorData.on_set += threshold_check
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
    # For the timed mode, listen for this few messages
    # AC state change command
    # Mode change command
    # Set new time period/new timeout


# Running code in the last block to make sure all funcs and vars are defined prior to use.
if __name__ == "__main__":
    # Only run main code if module called as the program entry point.


    # Everytime the interval time is successfully updated, the Pi will produce and publish a new Event.
    intervalTime.on_set += func # Make this into a decorator of some sort to use the above function
    # Everytime the interval time is successfully updated, Pi_controller needs to restart the loop
    intervalTime.on_set += restart_loop # Make this into a decorator of some sort to use the above function
    


    # Call the readData function every "intervalTime" to update the sensor Data and store the reference to this loop in a global variable
    intervalTimerRef = setInterval(intervalTime.value, readData)


    """ Attach callback functions defined above to the interval time variable
    
        Create a subscription to the 'Commands' topic:
        Attach the parse message functions inside the other module as Callback to the subscription

        Call the manual mode to be initialized and then wait....	
    """


    # Start the manual mode as the default mode
    mode_man()

    # Do nothing, pause and wait for events to happen.
    # Call the wait function to stop main thread from ending before the daemonic threads finnish
    wait_for_daemons() # Blocking call at the end of the main thread execution.