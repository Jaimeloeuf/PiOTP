from time import sleep
from threading import Timer

# GLobal variable used to store the reference to the current running timer.
t = None


def setInterval(sec, fn):
	# Use the global 't' variable for the scope of the setInterval function
	global t
	# Inner function that will be called when time outs

	def fn_wrapper():
		global t  # Use the global 't' variable for the scope of the fn_wrapper function
		# Call the original function
		fn()
		# Create another setTimeOut function, to call this function again.
		t = Timer(sec, fn_wrapper)
		# Start the timer
		t.start()

	# Create setTimeOut function, that will call the fnWrapper after set time
	t = Timer(sec, fn_wrapper)
	# Start the timer
	t.start()
	return t

"""  Example Usage:

	# Function to schedule
	def hi():
		print('hi')

	# Create interval of 1 second and call hi function
	timer = setInterval(1, hi)
	
	# To stop the interval: Access the global timer object and kill timer at anytime/anywhere
	timer.cancel()

"""
