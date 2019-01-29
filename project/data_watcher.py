"""	@Todos
    - Implement a method to allow user to change the sequence in which the listeners are executed in
    - Perhaps a method to allow all the callback functions to be executed concurrently in multiple threads.
    - Implement a show all listener method
    - Implement a remove listener method
        - By probably using a ID that is associated with the enumeration of the callback(s) array
"""

from threading import Thread
from multiprocessing import Process, process


class watch:
    __cbs = []

    def __init__(self, data):
        self.__data = data

    def set(self, data):
        self.__data = data
        print('Set function called')
        self.__event()
        return self

    def get(self):
        return self.__data

    def addListener(self, cb):
        self.__cbs.append(cb)
        return self

    def removeListener(self, cb=None):
        # To implement the second part where only the specified callback function is removed.
        self.__cbs.clear()  # Not sure if this method works, needs to be tested
        return self

    def __event2(self):
        # Should call all the callbacks in sperate threads/processes
        for cb in self.__cbs:
            cb()

    def __run_callbacks(self):
        # create and start our threads
        threads = []
        # Loop through and run all the callbacks as seperate threads
        for cb in self.__cbs:
            thread = Thread(target=cb)
            thread.daemon = True
            threads.append(thread)
            thread.start()

        # wait for all the threads to finish using (join)
        for thread in threads:
            # Blocking call till all the threads are done.
            thread.join()

    def __event(self):
        # All the callback functions should be pure functions with no external scoped dependencies
        cb_process = Process(target=self.__run_callbacks)
        cb_process.daemon = True
        cb_process.start()

        # Do I need to join??
        cb_process.join()


# If this module is called as a standalone module to run, then execute the example code
if __name__ == "__main__":
    from time import sleep

    # Create a new data variable and store in the watchData object
    sensorData = watch(36349)
    # The data stored in the object can only be accessed via the get method
    print(sensorData.get())

    # Below are 3 different callbacks that should run when the data changes
    def hi():
        print('hello world')

    def hi2():
        print('hello')

    def hi3():
        print('world')

        # Add the callbacks to the object
    sensorData.addListener(hi)
    sensorData.addListener(hi2)
    sensorData.addListener(hi3)

    # Add a time delay to simulate real life operations
    sleep(2)
    # Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(5)
    # Print out the updated value stored in the object.
    print(sensorData.get())

    # Add a time delay to simulate real life operations
    sleep(2)
    # Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(5)
    # Print out the updated value stored in the object.
    print(sensorData.get())

    while True:
        pass

    """ The first time u "set" a value, or should I say, watch the value, nothing happens at all. No callback, nothing.
        However when u set the variable with the exact same value, it still runs all the callbacks. Is this good or is this bad?
        Should data watcher's callbacks run when the value is changed, or when set method is called??
        
        So when I use this the publish data thing, when the data is still the same, do I want the data to be published?
        
        OH!!
        
        Maybe I can have 2 types of callbacks!
        a proprety created by decoroators and
        
        one called on_set and one called on_change
        
        then u can do something like,
        data.on_set += cb
        data.on_change += cb


        """
