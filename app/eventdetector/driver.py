import os
from eventhandler.listener import Receiver
from detective import Detective

BROKER_CLIENT_ID = os.environ['BROKER_CLIENT_ID']

if __name__ == '__main__':
    receiver = Receiver()
    detective = Detective()
    while True:
        try:
            for msg in receiver.readMqtt():
                detective.inspect(msg)
        except KeyboardInterrupt:
            break
