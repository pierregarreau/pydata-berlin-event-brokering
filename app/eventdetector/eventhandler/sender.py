import paho.mqtt.publish as publish
import time
import os
from json import dumps

BROKER_SERVER_IP = os.environ.get('BROKER_SERVER_IP')


class Publisher():
    def __init__(self, publisher_id, publisher_channel):
        self.id = publisher_id
        self.channel = "{channel}".format(channel=publisher_channel)
        self.last_msg_published = {}

    def publish(self, event_type, event_content):
        publish_topic = "{channel}/{type}/{id}".format(channel=self.channel, type=event_type, id=self.id)
        event = {
            'header': {
                'type': event_type,
                'ts': int(time.time()),
                'id': self.id
            },
            'body': event_content
        }
        publish.single(publish_topic, dumps(event), hostname=BROKER_SERVER_IP)
