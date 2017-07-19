#!/usr/bin/env python3.5
# coding=utf-8

from transitions import Machine
from typing import Dict

from eventhandler.sender import Publisher

MOVING = 'moving'
RESTING = 'resting'


class Boat():
    states = [MOVING, RESTING]

    def __init__(self, boat_id):
        self.id = boat_id
        self.position = {
            'ts': 0,
            'x': 0.0,
            'y': 0.0
        }
        self.init_state_machine()
        self.init_publisher()

    def init_state_machine(self) -> None:
        self._statemachine = Machine(model=self, states=Boat.states, initial=MOVING, after_state_change='_after_transition')
        self._register_transitions()

    def init_publisher(self) -> None:
        # event publishing
        self._publisher = Publisher(publisher_id=self.id, publisher_channel='EVENT')

    def _register_transitions(self) -> None:
        self._statemachine.add_transition('_transition_trigger', MOVING, RESTING, conditions='_is_resting')
        self._statemachine.add_transition('_transition_trigger', RESTING, MOVING, conditions='_is_moving')

    def _after_transition(self, context) -> None:
        self._publish(context)

    def _publish(self, position) -> None:
        port_id = position['port_id']
        event_content = {
            'boat_id': self.id,
            'state': self.state,
            'position': position
        }
        self._publisher.publish(
            event_type='{port_id}/STATETRANSITION'.format(port_id=port_id),
            event_content=event_content
        )

    def _is_moving(self, position):
        return (position['x'] != self.position['x']) or (position['y'] != self.position['y'])

    def _is_resting(self, position: Dict) -> bool:
        return (position['x'] == self.position['x']) and (position['y'] == self.position['y'])

    def update(self, position: Dict) -> None:
        self._transition_trigger(position)
        self.position = position
