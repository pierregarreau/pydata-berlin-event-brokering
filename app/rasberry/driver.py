from time import sleep
import os
from sender import Client
from simulator import DataGenerator

BROKER_CLIENT_ID = os.environ['BROKER_CLIENT_ID']

if __name__ == '__main__':
    client = Client(BROKER_CLIENT_ID)
    generator = DataGenerator()
    while True:
        try:
            position = generator.get_next()
            client.publish(position)
            sleep(0.5)
        except KeyboardInterrupt:
            break
