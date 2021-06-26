#!/usr/bin/env python3

import json
import influxdb
import time

from lennox_lcc import Client, LCC
from settings import *


client = Client("influxdb_importer", IP)
client.command({
    "systemControl": {
        "diagControl": {
            "level": 2
        }
    }
})
client.request_data(["/devices", "/equipments", "/zones"])


lcc = LCC()

influx = influxdb.InfluxDBClient(host=INFLUXDB_HOSTNAME, database=INFLUXDB_DATABASE)


def log_diagnostics(lcc: LCC):
    metrics = set()
    measurements = []
    for equipment in lcc.equipments.values():
        for d in equipment.diagnostics.values():
            if d.name in ("Cooling Rate", "Heating Rate", "Indoor Blower Power"):
                measurement_name = d.name.lower().replace(" ", "_")
                if measurement_name in metrics:  # 2 Heating Rate
                    measurement_name = measurement_name + "_2"
                metrics.add(measurement_name)
                measurements.append({
                    "measurement": "%",
                    "tags": {
                        "domain": "sensor",
                        "entity_id": measurement_name
                    },
                    "fields": {
                        "value": float(d.value)
                    }
                })
    influx.write_points(measurements, time_precision='s')


def log_zonestatus(lcc: LCC):
    measurements = []
    for zone in lcc.zones.values():
        if zone.temperature > 0:
            measurements.append({
                "measurement": "°F",
                "tags": {
                    "domain": "sensor",
                    "entity_id": "ChillCat_temp_2"
                },
                "fields": {
                    "value": float(zone.temperature)
                }
            })
        if zone.humidity > 0:
            measurements.append({
                "measurement": "%",
                "tags": {
                    "domain": "sensor",
                    "entity_id": "ChillCat_humidity_2"
                },
                "fields": {
                    "value": float(zone.humidity)
                }
            })
    influx.write_points(measurements, time_precision='s')

def log_system_status(lcc: LCC):
    measurements = []

    temp = lcc.systemStatus.outdoorTemperature
    if temp > 0:
        measurements.append({
            "measurement": "°F",
            "tags": {
                "domain": "sensor",
                "entity_id": "ChillCat_outdoor_temp"
            },
            "fields": {
                "value": float(temp)
            }
        })
    influx.write_points(measurements, time_precision='s')

for message in client.messages():
    if "Data" in message:
        lcc.load_data(message["Data"])
        if "equipments" in message["Data"]:
            log_diagnostics(lcc)

        elif "zones" in message["Data"]:
            # log_zonestatus(lcc)
            pass

        elif "system" in message["Data"] and "status" in message["Data"]["system"]:
            log_system_status(lcc)
    #print(json.dumps(message, indent=4, sort_keys=True))
