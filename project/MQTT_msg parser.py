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

# Should I make all of the incoming messages url encoded? So I can just use any library or smth to parse
	it for me instead of writing my own parser and switcher function.
# Learn how to use docker to automate all the installation and everything. This is a great opportunity to learn docker!
# Put my project description and everything up online too, so ppl know what the project I am woring on is about.
# should there be different parsers based on which mode is currently operating?

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

	mode=timed;
		!!! Timed mode means, on for a set time, or on for a specific time of the day.
		In the timed mode, another message will be expected

* When in timed mode, incoming messages that does not change mode or ac state are the following to control the timed mode actions

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
"""