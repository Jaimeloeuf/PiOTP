from time import sleep
from data_watcher import Watch

data = Watch(20)
print(data.get())


# Below are 3 different callbacks that should run when the data changes
def hi():
    print('hello world')


def hi2():
    print('hello')


def hi3():
    print('world')



# Add the callbacks to the object
data.addListener(hi)
data.addListener(hi2)
data.addListener(hi3)


def chicken():
    print('Inner func as event handler')


data.addListener(chicken)

# Add a time delay to simulate real life operations
sleep(1.4)
# Update the data in the object, this will cause all the callbacks to be called.
data.set(5)
# Print out the updated value stored in the object.
print(data.get())

# Add a time delay to simulate real life operations
sleep(1.4)
# Update the data in the object, this will cause all the callbacks to be called.
data.set(5)
# Print out the updated value stored in the object.
print(data.get())
