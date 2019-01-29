import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

class BME_Data:
	def __init__(self):
		self.read_data()

	def read_data(self):
		# the sample method will take a single reading and return a
		# compensated_reading object
		data = bme280.sample(bus, address, calibration_params)
		self.temperature = data.temperature
		self.humidity = data.humidity
		self.pressure = data.pressure
		# For a data-logger like application, periodically call above code to get time-based readings.

	@temperature.getter
	def temperature(self, formatted=False):
		if formatted:
			# return "{}C".format(self.temperature)
			return f'{self.temperature}°C'
		return self.temperature


	@humidity.getter
	def humidity(self, formatted=False):
		if formatted:
			return f'{self.humidity}%'
		return self.humidity


	@pressure.getter
	def pressure(self, formatted=False):
		if formatted:
			return f'{self.pressure} hPa'
		return self.pressure


"""
The compensated_reading class has the following attributes
	data.id
	data.timestamp
	data.temperature
	data.pressure
	data.humidity

To use the handy string representation
	print(data)

Sample expected data output:
	ee50df9c-3aa3-4772-8767-73b6bb74f30f
	2016-11-18 17:33:28.937863
	20.563
	980.91
	48.41
	compensated_reading(id=ee50df9c-3aa3-4772-8767-73b6bb74f30f,
		timestamp=2016-11-18 17:33:28.937863, temp=20.563 °C,
		pressure=980.91 hPa, humidity=48.41 % rH)
"""

if __name__ == "__main__":
    # If this module called as a standalone module to see how it works, then run the below example code
	BME_Data()