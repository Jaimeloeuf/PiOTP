from threading import Timer

""" @Todos
	- Create a method that will call the stop method when the process exits. Because the timer thread continues to run
	  even if the main program/thread is killed by keyboard interrupt, which means that the stop method is never called.
	- Create a method that allows user to specify if the interval should start running immediately. Meaning that I can create
	  the interval and store the reference first without letting it run, this is so to allow me to do some settings/changes to
	  the object first, or to allow user to only execute this 'loop' when certain conditions are met.
	- Create a method/check for the user to specify how many times this interval should run. So example would be, I only
	  want this interval based loop to loop a maximum of 10 times before I want it to automatically stop.
	  Or perhaps a time limit for how long this loop should loop for, like loopFor(10mins), meaning after 10 mins, the loop
	  should call self.stop method. This can be possibly implemented by using another 'kill interval' timer that calls the
	  stop method upon timeout.
	- Should I perhaps modify all the attributes/object-fields to be 'hidden' or 'private'? To prevent user from directly
	  accessing the data in the object, which might potentially cause the object to fail?
"""

class setInterval:
	# To pass in the interval time, callback function, and any arguements for the callback function into the constructor
	def __init__(self, time, fn, *args, **kwargs):
		self.time = time
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		# Instead of calling method on object creation, wait till end of the 1st time interval before calling method
		# Delay the first call to the timeout method by the given time interval
		Timer(self.time, self.timeOut).start()

	# Method that is run everytime the Timer time's out.
	def timeOut(self):
		# Call the given function with any arguements supplied
		self.fn(*self.args, **self.kwargs)
		# Create another Timer object, to call this function again on timeout.
		self.__t = Timer(self.time, self.timeOut)
		self.__t.start()

	# Method to stop the loop, if needed, execute the callback one last time
	def stop(self, oneLastTime=False):
		# Kill the timer that repeatedly calls the timeOut method.
		self.__t.cancel()
		# If 'oneLastTime' is True, Call the given function with any arguements supplied for the last time.
		if oneLastTime:
			self.fn(*self.args, **self.kwargs)

	# Set/Change the interval for which the timer takes to timeout. New interval will start immediately.
	def set_interval(self, time):
		# Stop the current timer
		self.stop()
		# Set the time into the object's field
		self.time = time
		# Delay the first call to the timeout method by the given time interval
		Timer(self.time, self.timeOut).start()

	# Set the arguements to be passed into the callback function
	def set_args(self, *args, **kwargs):
		# Set the input arguements into the object's fields.
		self.args = args
		self.kwargs = kwargs

if __name__ == "__main__":
	# If this module called as a standalone module to see how it works, then run the below example code
	from time import sleep

	def hi(val):
		print(val)

	tout = setInterval(1, hi, 'hei')
	sleep(6)
	# Stop the interval, but execute the callback one last time before killing the loop
	tout.stop(True)
