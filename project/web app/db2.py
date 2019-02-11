import argparse
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import time
import random

USER = 'root'
PASSWORD = 'root'
DBNAME = 'sensordata'
HOST = 'localhost'
PORT = 8086


def getSensorData():
    sensorData = random.randint(10, 45)
    now = time.gmtime()
    pointValues = [
        {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
            "measurement": 'reading1',
            "tags": {
                "nodeId": "node_1",
            },
            "fields": {
                "value": sensorData
            },
        }
    ]

    return(pointValues)


if __name__ == '_main_':
    dbclient = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    while True:
        data_point = getSensorData()
        dbclient.write_points(data_point)
        print("Written data")
        time.sleep(0.5)



def write(data):
    now = time.gmtime()
    pointValues = [
        {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
            "measurement": 'reading1',
            "tags": {
                "nodeId": "node_1",
            },
            "fields": {
                "value": sensorData
            },
        }
    ]
    dbclient.write_points(pointValues)