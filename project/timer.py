from threading import Timer

"""  Example Usage:

	# Create a new interval of 5 seconds executing the function, fn
	interval1 = setInterval(5, fn)

	# Stop the interval
	interval1.stop()
"""


# class setTinterval():
#     def __init__(self, sec, fn):
#         # Create setTimeOut function, that will call the fnWrapper after set time
#         self.sec = sec
#         self.fn = fn
#         self.t = Timer(sec, self.fn_wrapper)
#         # Start the timer
#         self.t.start()

#     def fn_wrapper(self):
#         self.fn()
#         self.t = Timer(self.sec, self.fn_wrapper)
#         # Start the timer
#         self.t.start()

#     def stop(self):
#         self.t.cancel()


class setInterval:
    def __init__(self, time, fn, *args, **kwargs):
        self.time = time
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        # Instead of starting the function on object creation, wait till the end of the 1st interval before calling the function
        # self.start() # Call the function the first time
        # Delay the first call by the given time interval
        Timer(self.time, self.timeOut).start()
	
    # Method that is run everytime the Timer time's out.
    def timeOut(self):
        # Call the given function with any arguements supplied
        self.fn(*self.args, **self.kwargs)
        # Create another Timer object, to call this function again on timeout.
        self.__t = Timer(self.time, self.timeOut)
        self.__t.start()

    def stop(self, oneLastTime=False):
        # Kill the timer that repeatedly calls the timeOut method.
        self.__t.cancel()
        # If 'oneLastTime' is True, Call the given function with any arguements supplied for the last time.
        if oneLastTime:
            self.fn(*self.args, **self.kwargs)

# exec()
# ^ Learn abt above


if __name__ == "__main__":
    # If this module called as a standalone module to see how it works, then run the below example code
    from time import sleep

    def hi(val):
        print(val)

    tout = setInterval(1, hi, 'hei')
    sleep(6)
    tout.stop()


# """  Example Usage:

# 	# Function to schedule
# 	def hi():
# 		print('hi')

# 	# Create interval of 1 second and call hi function
# 	timer = setInterval(1, hi)

# 	# To stop the interval: Access the global timer object and kill timer at anytime/anywhere
# 	timer.cancel()

# """
