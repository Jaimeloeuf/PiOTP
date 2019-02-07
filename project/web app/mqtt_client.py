""" Dependencies """
from JQTT import Publisher, Subscription
from db import write

""" Callback function definitions """
def on_data(data):
    # Add data into the Sensor Data DB
    write(data, 'SensorDB')


def on_ac_state(state):
    # Add data into the AC state DB
    write(state, 'ACstateDB')


# The entry point function. Will be ran as a subprocess from the server module
def start_sub():
    """ Create all the Subscriptions and attach the callback handlers """
    s = Subscription('IOTP/grp4/channel/SenD', on_connect=True, on_message=on_data)
    ac_state = Subscription('IOTP/grp4/channel/ac_state', on_connect=True, on_message=on_ac_state)
    