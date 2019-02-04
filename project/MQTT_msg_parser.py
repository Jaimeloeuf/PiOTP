# Callback function for MQTT subscriptions that parses incoming messages into their individual kv pairs
def parse_payload(payload):
    # Split the payload into their differet key value pairs
    properties = payload.split(';')
    # Loop through each key value pair
    for prop in properties:
        # Split each property into a list with a key and value
        prop = prop.split('=')
        # Verify kv pair and Log out the error if verification failed.
        if not verify(prop):
            print("Error: verification of kv pair from MQTT sub failed.")


# Given the kv pairs parsed out from abv function verify that they are valid?
def verify(prop):
    # Get the key, value pair out of the list
    key = prop[0]
    val = prop[1]
    # Remove white spaces for both the key and value
    for val in prop:
        # See which one works?
        val = val.strip()
        prop[val] = val.strip()
    # If the key is a valid key
    if key in commands:
        if set_state(key, val):
            # If true returned to indicate success, let it bubble up
            return True
    # If set_state returned false or if key not valid, return false to indicate failure
    return False

# Given the kv pairs from abv function set state to the Pi


def set_state(set_this, to_this):
    if set_this == None or to_this == None:
        return False
    elif set_this == 'mode':
        ac.set_mode()


""" The below will be set by the different modes. Every time the mode changes with
    a message from MQTT sub, execute/call the init function of that mode. """
def change_mode(mode):
    if mode == 'auto':
        return mode_auto()
    elif mode == 'man':
        return mode_man()
    elif mode == 'timed':
        return mode_timed()
    else:
        # Print/Log error
        print('Invalid mode is being passed')
        return False  # Return false to indicate error and operation failure

def ac_state(state):
    if mode == 'on':
        return mode_auto()
    elif mode == 'off':
        return mode_man()
    elif mode == 'on x':
        # Where x is the time to be on for
        return mode_timed()
    else:
        # Print/Log error
        print('Invalid AC state received')
        # Return false to indicate error and operation failure
        return False


# Function to change interval time variable. Interval span can be changed by the User via MQTT
def setIntervalTime(time):
    # Function will be ran on message received.
    intervalTime.set(time)


dispatch = {
    "mode": change_mode,
    "ac": ac_state,
    "interval time" setIntervalTime,
    # "time": 
}

if command in dispatch:
    # Either return it or respond to it.
    return dispatch[command](args)