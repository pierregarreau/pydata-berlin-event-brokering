
from json import loads
from statemachine.boat import Boat


class Detective():
    def __init__(self):
        self.boats = {}

    def inspect(self, msg):
        boat_msg = loads(msg)
        boat_id = boat_msg['boat_id']
        position = boat_msg['position']
        if not self.boats.get(boat_id):
            self.boats[boat_id] = Boat(boat_id)
        self.boats[boat_id].update(position)
