"""RPI 1 Wire temperature sensor."""

from nodestatman.domains import Domain
import glob


class OneWireTempDomain(Domain):
    """One wire temperature sensor domain."""

    _VALID_FIELDS = ['temperature']
    _DOMAIN = 'w1temp'

    def __init__(self, controller, scan_interval=60, **kwargs):
        """Initialize."""
        super().__init__(controller, **kwargs)
        self._scan_interval = scan_interval
        self._scan_timer = None

    def start_collecting(self):
        """Start collecting data."""
        self._scan_timer = self.timer_start(self._scan_interval,
                                            self._temp_scan)

    def stop_collecting(self):
        """Stop collecting data."""
        if self._scan_timer is not None:
            self.timer_cancel(self._scan_timer)

    def _temp_scan(self):
        base_dir = '/sys/bus/w1/devices/'
        device_folders = glob.glob(base_dir + '28*')
        device_files = [folder + '/w1_slave' for folder in device_folders]

        def read_raw(fname):
            with open(fname, 'r') as f:
                lines = f.readlines()
                return lines

        # read temperatures
        for idx, fname in enumerate(device_files):
            ret = read_raw(fname)
            success = ret[0].strip().endswith('YES')
            if success is False:
                continue

            temp_pos = ret[1].find('t=')
            if temp_pos == -1:
                continue

            temp_str = ret[1][temp_pos+2:]
            temp_c = float(temp_str) / 1000.0
            temp_f = temp_c*9.0/5.0 + 32.0
            self.commit_reading('temp{}'.format(idx), 'temperature', temp_f)
        return True


_DOMAINS = {OneWireTempDomain._DOMAIN, OneWireTempDomain}
