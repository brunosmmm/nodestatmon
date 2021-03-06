"""RPi GPIO"""

from gpiozero import MotionSensor
from nodestatman.domains import Domain


class MotionSensorDomain(Domain):
    """Motion sensor domain."""

    _DOMAIN = 'motionsens'
    _VALID_FIELDS = ['motion']

    def __init__(self, controller, gpionum=None, **kwargs):
        """Initialize."""
        super().__init__(controller, **kwargs)
        self._gpionum = gpionum
        self._sensor = MotionSensor(pin=gpionum)
        self._sensor_worker = None

    def start_collecting(self):
        """Start collecting data."""
        self._sensor_worker = self.install_worker(self._motion_detect)

    def stop_collecting(self):
        """Stop collecting data."""
        self.remove_worker(self._sensor_worker)

    def _motion_detect(self, stop_flag):
        """Motion detect loop."""
        state = 'wait_motion'
        while stop_flag.is_set() is False:
            # blocking motion sensing
            if state == 'wait_motion':
                wait = self._sensor.wait_for_motion(10)
                if wait is True:
                    self.push_reading('motion{}'.format(self._gpionum),
                                      'motion', 1)
                    state = 'wait_no_motion'
            else:
                wait = self._sensor.wait_for_no_motion(10)
                if wait is True:
                    self.push_reading('motion{}'.format(self._gpionum),
                                      'motion', 0)
                    state = 'wait_motion'


_DOMAINS = {MotionSensorDomain._DOMAIN: MotionSensorDomain}
