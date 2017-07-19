#!/usr/bin/env python3
# coding=utf-8

import os
import paho.mqtt.client as paho
import queue as q
from typing import Dict

BROKER_SERVER_IP = os.environ.get('BROKER_SERVER_IP')
BROKER_SERVER_PORT = os.environ.get('BROKER_SERVER_PORT')
BROKER_CLIENT_ID = os.environ.get('BROKER_CLIENT_ID')


class Receiver(object):
    def __init__(self, client_id=BROKER_CLIENT_ID, client_channel='DATA/#'):
        self.id = client_id  # unique
        self.queue = q.Queue()
        self.subscribe_channel = "{subscribe_channel}".format(subscribe_channel=client_channel)
        self.register_client()

    def __del__(self):
        self.client.loop_stop()
        self.disconnect_client()

    def register_client(self):
        self.client = paho.Client(client_id=self.id, clean_session=True)
        # callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.will_set('notifications',
                             payload='{id} ({name}) died.'.format(id=self.id, name=__name__),
                             qos=1,
                             retain=True)
        self.client.connect(BROKER_SERVER_IP, port=int(BROKER_SERVER_PORT))
        self.client.loop_start()

    def disconnect_client(self):
        self.client.disconnect()
        self.disconnect_paho_sockets()

    def disconnect_paho_sockets(self):
        try:
            self.client._sockpairR.close()
            self.client._sockpairW.close()
        except Exception as e:
            pass

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.subscribe_channel, qos=0)

    def on_message(self, client, userdata, message):
        data = message.payload.decode('ascii')
        try:
            self.queue.put(data.rstrip())
        except:
            pass

    def readMqtt(self):
        # generator
        for msg in iter(self.queue.get, None):
            massaged_event = self._massage_event(msg)
            if not massaged_event:
                continue
            yield(massaged_event)

    def _massage_event(self, msg: Dict) -> Dict:
        # massage the data here if needed
        return msg
