#!/usr/bin/env python3
import paho.mqtt.client as paho
import os
from json import dumps

BROKER_SERVER_IP = os.environ['BROKER_SERVER_IP']
BROKER_SERVER_PORT = int(os.environ['BROKER_SERVER_PORT'])


class Client(object):
    def __init__(self, client_id: int) -> None:
        self.id = client_id  # unique
        self.channel = 'DATA/{id}'.format(id=client_id)
        self.register_client()

    def __del__(self) -> None:
        self.disconnect_client()

    def disconnect_client(self)-> None:
        self.client.loop_stop()
        self.client.disconnect()
        self.disconnect_paho_sockets()

    def disconnect_paho_sockets(self) -> None:
        try:
            self.client._sockpairR.close()
            self.client._sockpairW.close()
        except Exception as e:
            pass

    def register_client(self) -> None:
        self.client = paho.Client(client_id=self.id, clean_session=True)
        self.client.will_set('notifications', payload='{name} {id} died.'.format(id=self.id, name=__name__), qos=1,
                             retain=True)
        self.connect_client()
        self.client.loop_start()

    def connect_client(self) -> None:
        self.client.connect(host=BROKER_SERVER_IP, port=BROKER_SERVER_PORT)

    def publish(self, event) -> None:
        self.client.publish(self.channel, payload=dumps(event), qos=1)
