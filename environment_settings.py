# Copy to settings.py and update accordingly
from os import environ

IP = environ.get("IP", "192.168.1.50")          # the IP of the S60 Smart Hub wifi
CLIENT_ID = environ.get("CLIENT_ID", "python_client")  # whatever you want it to be

INFLUXDB_HOSTNAME = environ.get("INFLUXDB_HOSTNAME", "localhost")
INFLUXDB_PORT = int(environ.get("INFLUXDB_PORT", "8086"))
INFLUXDB_DATABASE = environ.get("INFLUXDB_DATABASE", "home_assistant")
