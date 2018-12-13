"""Wifi domain."""

from nodestatman.domains import Domain
from wifi import Cell


class WifiDomain(Domain):
    """Wifi domain."""

    _VALID_FIELDS = ['signal', 'quality', 'bitrates', 'channel']
    _DOMAIN = 'wifi'

    def __init__(self, controller, scan_interval=30, ssids=None, interface=None,
                 report=['signal', 'quality'], **kwargs):
        """Initialize."""
        super().__init__(controller, **kwargs)
        self._scan_interval = scan_interval
        if ssids is None:
            raise RuntimeError
        elif isinstance(ssids, (list, tuple)):
            for name in ssids:
                self.register_instance(name)
        elif isinstance(ssids, str):
            self.register_instance(ssids)
            ssids = [str]
        self._ssids = ssids
        self._iface = interface

        for field in report:
            if field not in self._VALID_FIELDS:
                raise KeyError
        for field in report:
            self.register_field(field)
        self._report_fields = report
        self._wifi_scan_timer = None

    def start_collecting(self):
        """Start collecting."""
        self._wifi_scan_timer = self.timer_start(self._scan_interval,
                                                 self._wifi_scan)

    def stop_collecting(self):
        """Stop collecting."""
        if self._wifi_scan_timer is not None:
            self.timer_cancel(self._wifi_scan_timer)

    def _wifi_scan(self):
        print('wifi scan')
        result = Cell.all(self._iface)
        for cell in result:
            if cell.ssid in self._ssids:
                # commit readings
                for field in self._report_fields:
                    self.commit_reading(cell.ssid, field, getattr(cell, field))
        return True


_DOMAINS = {WifiDomain._DOMAIN: WifiDomain}
