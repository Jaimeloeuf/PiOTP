from influxdb import InfluxDBClient

# Create a client that connects to the DB over HTTP
client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='SensorDB')
# Instruct the DB to create a DB named 'SensorDB'
client.create_database('SensorDB')

# Get the list of databases in InfluxDB as a list of dictionaries
dbs = client.get_list_database()
print(dbs)



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




# Ask client to close the HTTP connection to the DB server
client.close()