from influxdb import InfluxDBClient

# Create a client that connects to the DB over HTTP
client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='SensorDB')

# Get the list of databases in InfluxDB as a list of dictionaries
def get_dbs():
	return client.get_list_database()

def create_db(DB):
	# Instruct the DB to create a DB named 'SensorDB'
	client.create_database(DB)

query = 'select value from cpu_load_short;'
json_body = [
	{
		"measurement": "cpu_load_short",
		"tags": {
			"host": "server01",
			"region": "us-west"
		},
		"time": "2009-11-10T23:00:00Z",
		"fields": {
			"Float_value": 0.64,
			"Int_value": 3,
			"String_value": "Text",
			"Bool_value": True
		}
	}
]


# Function to write data to the DataBase. DB defaults to SensorDB
def write(data, DB='SensorDB'):
	client.write_points



# Ask client to close the HTTP connection to the DB server
client.close()


if __name__ == "__main__":
	# Create the DB
	create_db('SensorDB')