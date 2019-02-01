from threading import Thread


class Watch:
    # __on_set_cbs callback functions run the moment set method is used to set a value to the variable.
    __on_set_cbs = []
    # __on_change_cbs callback functions only run if the new value set is different from the previous value.
    __on_change_cbs = []

    def __init__(self, data):
        self.__data = data

    # Method to set a value to the data variable watched by this class
    def set(self, data):
        # If set is called and data value has been changed, save the data and run on change callbacks
        if data != self.__data:
            self.__data = data
            # Call all the __on_change_cbs callback functions
            self.__event(self.__on_change_cbs)

        # Regardless of data, call all the __on_set_cbs callback functions when set method called.
        self.__event(self.__on_set_cbs)
        # Return self reference to allow method call chainings.
        return self

    # Decorated Method to use as an attribute to get watched/stored data
    @property
    def value(self):
        return self.__data

    # Method to append a new callback function to be ran when the set method is called
    def on_set(self, cb):
        self.__on_set_cbs.append(cb)
        # Return self reference to allow method call chainings.
        return self

    # Method to append a new callback function to be ran when the watched data is changed
    def on_change(self, cb):
        self.__on_change_cbs.append(cb)
        # Return self reference to allow method call chainings.
        return self

    def removeListener(self, cb=None):
        # To implement the second part where only the specified callback function is removed.
        # self.__cbs.clear()  # Not sure if this method works, needs to be tested
        # Return self reference to allow method call chainings.
        return self

    def __event(self, callbacks):
        # Loop through and run all the callbacks as seperate threads
        for cb in callbacks:
            Thread(target=cb, daemon=True).start()


# If this module is called as a standalone module to run, then execute the example code
if __name__ == "__main__":
    # Dependencies for the example code.
    from time import sleep
    import threading

    # Create a new data variable and store in the watchData object
    sensorData = Watch(36349)
    # The data stored in the object can only be accessed via the value property
    print(sensorData.value)

    # Below are 3 different callbacks that should run when the data changes
    def hi():
        sleep(2.5)
        print('hello world')

    def chicken():
        sleep(0.2)
        print('Chicken nuggets')

    def on_change_cb():
        print('The value has been changed')

    # Add the callbacks to the object
    sensorData.on_set(hi)
    sensorData.on_set(chicken)
    sensorData.on_change(on_change_cb)

    # Add a time delay to simulate real life operations
    sleep(1.4)
    # Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(1)
    # Print out the updated value stored in the object.
    print(sensorData.value)

    # Add a time delay to simulate real life operations
    sleep(1.4)
    # Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(2)
    # Print out the updated value stored in the object.
    print(sensorData.value)

    # Add a time delay to simulate real life operations
    sleep(1.4)
    # Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(2)
    # Print out the updated value stored in the object.
    print(sensorData.value)


    # Function that waits for all the daemon threads to end by calling join method on them.
    def daemon_thread_join():
        # Wait for all daemonic threads to end before ending the main thread, which will kill any still-alive daemonic threads.
        for thread in threading.enumerate():
            if thread.daemon:
                thread.join()

    daemon_thread_join()