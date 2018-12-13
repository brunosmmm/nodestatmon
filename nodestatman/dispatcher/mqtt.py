"""MQTT Dispatcher."""

from nodestatman.dispatcher import Dispatcher, DispatcherOptionError
import paho.mqtt.client as mqtt
import socket


class MQTTDispatcher(Dispatcher):
    """MQTT Dispatcher."""

    def __init__(self, controller, unitname=None, prefix=None, address=None, **kwargs):
        """Initialize."""
        super().__init__(controller, **kwargs)
        self._client = mqtt.Client()
        if unitname is None:
            raise DispatcherOptionError('invalid unit name')
        if prefix is None:
            raise DispatcherOptionError('invalid prefix')
        if address is None:
            raise DispatcherOptionError('option address is required')
        self._unitname = unitname
        self._prefix = prefix
        self._address = address

    def start_dispatching(self):
        """Start dispatching."""
        self._client.connect(self._address)
        self._client.loop_start()

    def stop_dispatching(self):
        """Stop dispatching."""
        self._client.loop_stop()

    def dispatch_commit(self, domain, instance, field, value):
        """Dispatch a value commit."""
        self._client.publish('{}/{}/{}/{}/{}'.format(
            self._prefix,
            self._unitname,
            domain,
            field,
            instance), value)
