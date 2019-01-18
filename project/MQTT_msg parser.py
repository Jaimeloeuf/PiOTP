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


"""	List of possible valid messages that will be received from the MQTT broker

* Everytime the state of the AC is changed, it should use the MQTT lib to publish the change.

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

	mode=timed;time=x;
		!!! Timed mode means, on for a set time, or on for a specific time of the day.
		Turn the AC on regardless of current state.
		Create a timer to countdown with the given time to off the AC after that, if at anypoint, the
		ac is offed, or this mode is 'turned off' then kill the timer

	mode=timed;start=x;end=y;
		!!! Timed mode means, on for a set time, or on for a specific time of the day.
		Change the mode to timed, and disable everything and just wait for the start time, --> use a event thing or smth for the start time
		when it is start time, on the AC and wait for the end time
		when it is the end time, off the AC and put the system into timed mode doing nth and waiting for a new time?

	start=x;end=y;
		This command is only valid if the current mode is timed,
		do the abv actions with this new set of 'time zone'


mode is basically choosing which "pi controller" to use to control the pi's ac
"""