"""	@Todos
	- Implement a method to allow user to change the sequence in which the listeners are executed in
	- Implement a show all listener method
	- Implement a remove listener method
"""

class watch:
    __cbs = []

    def __init__(self, data):
        self.__data = data

    def set(self, data):
        self.__data = data
        self.__event()

    def get(self):
        return self.__data

    def addListener(self, cb):
        self.__cbs.append(cb)

    def __event(self):
        for cb in self.__cbs:
            cb()


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
    sleep(4)

	# Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(5)
	# Print out the updated value stored in the object.
    print(sensorData.get())

	# Add a time delay to simulate real life operations
    sleep(4)

# Trigger when set function called, or when the valus is set, or when the value different from the value inside now

	# Update the data in the object, this will cause all the callbacks to be called.
    sensorData.set(5)
	# Print out the updated value stored in the object.
    print(sensorData.get())