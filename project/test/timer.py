from time import sleep
from threading import Timer
import os
import psutil

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


def hi():
    val = (psutil.Process(os.getpid()).memory_info().rss) / 1024 / 1024  # in KB
    print(val)


setInterval(1, hi)
# Access the global timer object and kill timer at anytime/anywhere
t.cancel()


# class ThreadJob(threading.Thread):
#     def __init__(self, callback, event, interval):
#         '''runs the callback function after interval seconds

#         :param callback:  callback function to invoke
#         :param event: external event for controlling the update operation
#         :param interval: time in seconds after which are required to fire the callback
#         :type callback: function
#         :type interval: int
#         '''
#         self.callback = callback
#         self.event = event
#         self.interval = interval
#         super(ThreadJob, self).__init__()

#     def run(self):
#         while not self.event.wait(self.interval):
#             self.callback()


# event = threading.Event()

# k = ThreadJob(hi, event, 2)
# k.start()

# # setInterval(hi, 1)
# print('hi second')

# from asyncio import sleep, run

# async def setInterval(fn, time):
# 	timer = None
# 	while True:
# 		timer = await sleep(time) # Create an async wait timer
# 		fn()
# 	return timer

# run(setInterval(hi, 1))
# print('hi second')

# # import sched
# from sched import
