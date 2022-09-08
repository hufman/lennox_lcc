#!/usr/bin/env python3

import json
import requests
import time
import urllib3
from typing import Generator, Iterable

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
    def __init__(self, client_id: str, ip: str):
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

    def command(self, data: dict):
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

    def request_data(self, paths: Iterable[str]):
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

    def messages(self) -> Generator:
        running = True
        while running:
            resp = requests.get(f"https://{self.ip}/Messages/{self.client_id}/Retrieve", verify=False)
            if len(resp.text) == 0:
                time.sleep(1)
                yield {}
                continue

            for message in resp.json()["messages"]:
                yield message
