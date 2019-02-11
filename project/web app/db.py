from influxdb import InfluxDBClient
# Time module needed to create time stamps
import time


# Initialization function
def init():
    # Below are the hardcoded credentials of the DB. To be changed!
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'sensordata'
    HOST = 'localhost'
    PORT = 8086

    # Global variable to store the client object created by this init function
    global client
    # Create and attach the client object that connects to the DB over HTTP
    client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='SensorDB')


# Get the list of databases in InfluxDB as a list of dictionaries
def get_dbs():
    return client.get_list_database()

def create_db(DB):
    # Lookup and loop through all existing databases
    for db in get_dbs():
        # If the database with the same name already exists
        if DB == db:
            # Return False to indicate operation failure and skip creation
            return False
    
    # Else if none exists, instruct the DB to create a DB named 'SensorDB'
    client.create_database(DB)
    # Return True to indicate operation success
    return True


# Function to write data to the DataBase. DB defaults to SensorDB
def write(data, DB='SensorDB'):
    # Construct the data body that will be stored into the DB. To format it better!
    pointValues = [
        {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "measurement": 'reading1',
            "tags": {
                "nodeId": "node_1",
            },
            "fields": {
                "value": data
            },
        }
    ]
    # Send data to DB to store
    client.write_points(pointValues)


def disconnect():
    # Referencing the global client variable
    global client
    # If connected to DB and client object is valid
    if client != None:
        # Ask client to close the HTTP connection to the DB server
        client.close()
    # Reset the reference to the client object. Init func needs to be called again to use the DB
    client = None


if __name__ == "__main__":
    # Example/test code if ran as main module

    # Create the DB
    create_db('SensorDB')

    # query = 'select value from cpu_load_short;'