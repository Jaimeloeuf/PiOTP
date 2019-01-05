import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)

# there is a handy string representation too
print(data)

"""  Sample expected data output:
ee50df9c-3aa3-4772-8767-73b6bb74f30f
2016-11-18 17:33:28.937863
20.563
980.91
48.41
compensated_reading(id=ee50df9c-3aa3-4772-8767-73b6bb74f30f,
    timestamp=2016-11-18 17:33:28.937863, temp=20.563 °C,
    pressure=980.91 hPa, humidity=48.41 % rH)
"""

# For a data-logger like application, periodically call code below to get time-based readings.
# bme2.sample(bus, address, calibration_params)