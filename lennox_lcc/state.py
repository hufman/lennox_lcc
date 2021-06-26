#!/usr/bin/env python3

import json
import requests
import time
import urllib3
from typing import Dict


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

    def load_data(self, data: Dict):
        for diagnostic_data in data["diagnostics"]:
            d = self.diagnostics.setdefault(diagnostic_data["id"], Diagnostic())
            d.load_data(diagnostic_data["diagnostic"])

class SystemStatus:
    def __init__(self):
        self.outdoorTemperatureStatus = ""
        self.outdoorTemperature = -1
        self.outdoorTemperatureC = -1

    def load_data(self, data: Dict):
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

    def load_data(self, data: Dict):
        for key in dir(self):
            if key in data:
                setattr(self, key, data.get(key))

class LCC:
    def __init__(self):
        self.equipments = {}
        self.systemStatus = SystemStatus()
        self.zones = {}

    def load_data(self, data: Dict):
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
