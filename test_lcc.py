#!/usr/bin/env python3

import json
import requests
import time
from timeit import default_timer as timer
import urllib3

from settings import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
    def __init__(self, client_id, ip):
        self.client_id = client_id
        self.ip = ip
        self.message_id = 0
        self.connected = False

    def connect(self):
        requests.post(f"https://{self.ip}/Endpoints/{self.client_id}/Connect", verify=False).raise_for_status()
        self.connected = True

    def connect_if_necessary(self):
        if not self.connected:
            self.connect()

    def disconnect(self):
        requests.post(f"https://{self.ip}/Endpoints/{self.client_id}/Disconnect", verify=False).raise_for_status()
        self.connected = True

    def _generate_message_id(self):
        used = self.message_id
        self.message_id += 1
        return str(used)

    def command(self, data):
        body = {
            "MessageId": self._generate_message_id(),
            "MessageType": "Command",
            "SenderId": self.client_id,
            "TargetId": "LCC",
            "data": data,
            "AdditionalParameters": {
                "JSONPath": list(data.keys())[0]
            }
        }
        self.connect_if_necessary()
        requests.post(f"https://{self.ip}/Messages/Publish", json=body, verify=False).raise_for_status()

    def request_data(self, paths):
        body = {
            "MessageId": self._generate_message_id(),
            "MessageType": "RequestData",
            "SenderId": self.client_id,
            "TargetId": "LCC",
            "AdditionalParameters": {
                "JSONPath": f"1;{';'.join(paths)}"
            }
        }
        self.connect_if_necessary()
        requests.post(f"https://{self.ip}/Messages/RequestData", json=body, verify=False).raise_for_status()

    def messages(self):
        while True:
            start = timer()
            params = {
                "Direction": "Oldest-to-Newest",
                "MessageCount": "10",
                "StartTime": "1",
                "LongPollingTimeout": "15"
            }
            resp = requests.get(f"https://{self.ip}/Messages/{self.client_id}/Retrieve", params=params, verify=False)
            finished = timer()
            print(f"fetched message data in {finished - start:.3f}s")
            if len(resp.text) == 0:
                time.sleep(1)
                continue

            for message in resp.json()["messages"]:
                yield message


client = Client(CLIENT_ID, IP)
client.command({
    "systemControl": {
        "diagControl": {
            "level": 2
        }
    }
})
client.request_data(["/devices", "/equipments", "/zones"])


class Diagnostic:
    KEYS = ("valid", "name", "value", "unit")

    def __init__(self):
        self.valid = True
        self.name = ""
        self.value = ""
        self.unit = ""

    def load_data(self, data):
        for key in dir(self):
            if key in data:
                setattr(self, key, data.get(key))

class Equipment:
    def __init__(self):
        self.diagnostics = {}

    def load_data(self, data):
        for diagnostic_data in data["diagnostics"]:
            d = self.diagnostics.setdefault(diagnostic_data["id"], Diagnostic())
            d.load_data(diagnostic_data["diagnostic"])

class SystemStatus:
    def __init__(self):
        self.outdoorTemperatureStatus = ""
        self.outdoorTemperature = -1
        self.outdoorTemperatureC = -1

    def load_data(self, data):
        for key in dir(self):
            if key in data:
                setattr(self, key, data.get(key))

class ZoneStatus:
    def __init__(self):
        self.fan = False
        self.allergenDefender = False
        self.humidity = -1
        self.temperature = -1
        self.damper = -1
        self.heatCoast = False
        self.defrost = False
        self.humidityStatus = ""
        self.humOperation = ""
        self.balancePoint = ""
        self.tempOperation = ""
        self.ventilation = ""
        self.demand = -1
        self.aux = False
        self.coolCoast = False
        self.ssr = False
        self.temperatureStatus = ""
        self.temperatureC = -1

    def load_data(self, data):
        for key in dir(self):
            if key in data:
                setattr(self, key, data.get(key))

class LCC:
    def __init__(self):
        self.equipments = {}
        self.systemStatus = SystemStatus()
        self.zones = {}

    def load_data(self, data):
        if "equipments" in data:
            for equipment_data in data["equipments"]:
                e = self.equipments.setdefault(equipment_data["id"], Equipment())
                e.load_data(equipment_data["equipment"])
        if "system" in data and "status" in data["system"]:
            self.systemStatus.load_data(data["system"]["status"])
        if "zones" in data:
            for zone_data in data["zones"]:
                z = self.zones.setdefault(zone_data["id"], ZoneStatus())
                z.load_data(zone_data["status"])

lcc = LCC()

zone_status_keys = {
    "demand": "Demand",
    "humidity": "Humidity",
    "temperature": "Temperature"
}

for message in client.messages():
    try:
        if "Data" in message and "equipments" in message["Data"]:
            lcc.load_data(message["Data"])
            for equipment in lcc.equipments.values():
                for d in equipment.diagnostics.values():
                        print(f"{d.name}: {d.value} {d.unit}")

        elif "Data" in message and "zones" in message["Data"]:
            lcc.load_data(message["Data"])
            for zone in lcc.zones.values():
               for key, name in zone_status_keys.items():
                   print(f"{name}: {getattr(zone, key)}")

        elif "Data" in message and "system" in message["Data"] and "status" in message["Data"]["system"]:
            lcc.load_data(message["Data"])
            print(f"Outdoor Temperature: {lcc.systemStatus.outdoorTemperature}")
        #print(json.dumps(resp.json(), indent=4, sort_keys=True))
    except:
        print(resp.text)
        raise
    #time.sleep(1)
