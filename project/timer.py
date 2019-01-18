from time import sleep
from threading import Timer

"""  Example Usage:

	# Create a new interval of 5 seconds executing the function, fn
	interval1 = setInterval(5, fn)

	# Stop the interval
	interval1.stop()
"""

class setTinterval():
    def __init__(self, sec, fn):
        # Create setTimeOut function, that will call the fnWrapper after set time
        self.sec = sec
        self.fn = fn
        self.t = Timer(sec, self.fn_wrapper)
        # Start the timer
        self.t.start()

    def fn_wrapper(self):
        # Call the original function
        self.fn()
        # Create another setTimeOut function, to call this function again.
        self.t = Timer(self.sec, self.fn_wrapper)
        # Start the timer
        self.t.start()

    def stop(self):
        self.t.cancel()


# Code below is faced out for now in favour of the new class design
# """  Example Usage:

# 	# Function to schedule
# 	def hi():
# 		print('hi')

# 	# Create interval of 1 second and call hi function
# 	timer = setInterval(1, hi)

# 	# To stop the interval: Access the global timer object and kill timer at anytime/anywhere
# 	timer.cancel()

# """

# # GLobal variable used to store the reference to the current running timer.
# t = None

# # Function that calls the given function every 'sec' seconds
# def setInterval(sec, fn):
#     # Use the global 't' variable for the scope of the setInterval function
#     global t
#     # Inner function that will be called when time outs

#     def fn_wrapper():
#         global t  # Use the global 't' variable for the scope of the fn_wrapper function
#         # Call the original function
#         fn()
#         # Create another setTimeOut function, to call this function again.
#         t = Timer(sec, fn_wrapper)
#         # Start the timer
#         t.start()

#     # Create setTimeOut function, that will call the fnWrapper after set time
#     t = Timer(sec, fn_wrapper)
#     # Start the timer
#     t.start()
#     return t