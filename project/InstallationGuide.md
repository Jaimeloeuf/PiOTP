### Installing InfluxDB
##### Installing the DB itself
- Debian Based Linux:
	- wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.3_amd64.deb
	- sudo dpkg -i influxdb_1.7.3_amd64.deb
- Raspbian

- Docker
	- docker pull influxdb
- Windows
	- https://dl.influxdata.com/influxdb/releases/influxdb-1.7.3_windows_amd64.zip

##### Installing the Python Connector package
pip install influxdb