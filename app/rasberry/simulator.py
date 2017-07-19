import random
import time
import os
from scipy.stats import norm

BROKER_CLIENT_ID = os.environ['BROKER_CLIENT_ID']


class Boat():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.delta = 0.25
        self.ts_now = int(time.time())

    def get_position(self):
        dt = int(time.time()) - self.ts_now
        is_moving = (random.random() > 0.40)
        if is_moving:
            self.x += norm.rvs(scale=self.delta**2*dt)
            self.y += norm.rvs(scale=self.delta**2*dt)
        self.ts_now += dt
        return {
            'ts': self.ts_now,
            'x': self.x,
            'y': self.y,
            'port_id': BROKER_CLIENT_ID
        }


class DataGenerator():
    def __init__(self):
        self.boats = {
            1: Boat(),
            2: Boat(),
            3: Boat(),
            4: Boat()
        }
        self.num_boats = 4

    def get_next(self):
        key = random.randrange(self.num_boats) + 1
        return {
            'boat_id': key,
            'position': self.boats[key].get_position()
        }
