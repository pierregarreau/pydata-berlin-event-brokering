# The Broker: an event detection engine for the maritime industry

<a href="http://www.maritimedatasystems.com/"><img src="docs/img/tuganalytics.png" width=50px></a>

## Get started

To fire up the app, `cd` into the `app` folder and start `docker-compose`. This assumes you have docker installed. For a short introduction to docker, visit [this page](http://www.docker.com):

```
# docker-compose up --build -d
```

To monitor the actual event flow -- that is the incoming data from the rasberry Pi containers, and the internal messages exchanged in the main container -- you need to have [mosquitto](https://mosquitto.org) installed:

```
# apt-get install mosquitto-clients
```

To listen to the event stream replace <your_topic> with `DATA/#` or `EVENT/#`, for instance:

```
$ mosquitto_sub -h localhost -p 1883 -t 'EVENT/PYDATA_BERLIN_MEETUP-PORT2/#'
```

## Storytelling

This project is a showcase presented at [PyData-Berlin](https://www.meetup.com/PyData-Berlin/events/241567414/) on 2017-07-19. It shows how the MQTT protocol, originally developed for IOT applications, can also be used at a legitimate event broker within a (python) App.

We make use of two main libraries here:
* [eclipse-paho.mqtt](https://github.com/eclipse/paho.mqtt.python) for the message broker and;
* [pytransitions](https://github.com/pytransitions/transitions) for organizing event detection with state machines.

A basic description of main concepts is found below.

#### Publisher

paho-mqtt.python is a simple Publish / Subscribe message broker library implementing the MQTT protocol. Sending and receiving data is as straightforward as the two code snippets below.

```python
class Sender:
    def __init__(self, client_id):
        self.channel = 'data/{id}'.format(id=client_id)
        self.register_client()

    def register_client(self):
        self.client = paho.Client()
        self.client.connect()
        self.client.loop_start()

    def publish(self, event):
        self.client.publish(self.channel, payload=event, qos=1)
```

#### Subscriber

```python
class Receiver:
  def __init__(self, client_id):
    self.id = client_id
    self.queue = q.Queue()
    self.subscribe_channel = 'data/#'
    self.register_client()

  def register_client(self):
    self.client = paho.Client()
    self.client.on_connect = self.on_connect
    self.client.on_message = self.on_message
    self.client.connect()
    self.client.loop_start()

  def on_connect(self, client, userdata, flags, rc):
    self.client.subscribe(self.subscribe_channel, qos=1)

  def on_message(self, client, userdata, message):
    data = message.payload.decode('ascii')
    self.queue.put(data)
```

We warmly recommend the [README.md](https://github.com/pytransitions/transitions) showing how to get started with pytransitions. Below a minimal example.

#### Init state-machine

```python

MOVING='moving'
RESTING='resting'

class PublisherSM:
    states = [MOVING, RESTING]

    def __init__(self):
        self.init_state_machine()

    def init_state_machine(self):
        self._statemachine = Machine(model=self, states=PublisherSM.states, initial=MOVING)
        self._register_transitions()

    def _register_transitions(self):
        self._statemachine.add_transition('_transition_trigger', MOVING, RESTING, conditions='_is_resting')
        self._statemachine.add_transition('_transition_trigger', RESTING, MOVING, conditions='_is_moving')

    def _is_moving(self, position):
        return position['x'] != self.position['x'] or position['y'] != self.position['y']

    def _is_resting(self, position):
        return not self.is_moving(position)
```

We incorporated a publisher in the state-machines we use to organize our event flow, so that paho-mqtt becomes our internal message broker as well. Below an example of a two states (publishing) state-machine.

#### On transition

```python
class PublisherSM:
    def __init__(self):
      # [...]
      self.init_publisher()

    # [...]

    def init_publisher(self):
        self._publisher = Publisher(publisher_id=self.id, publisher_channel='EVENT')

    def _publish(self, context):
        event_content = {
            'state': self.state,
            'context': context
        }
        self._publisher.publish(event_type='STATETRANSITION', event_content=event_content)

    def _after_transition(self, context):
        self._publish(context)
```
