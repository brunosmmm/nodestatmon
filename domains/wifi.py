"""Wifi domain."""

from nodestatman.domains import Domain
from wifi import Cell


class WifiDomain(Domain):
    """Wifi domain."""

    def __init__(self, **kwargs):
        """Initialize."""
        super().__init__(scan_interval=30, interfaces=None, **kwargs)
        self._scan_interval = scan_interval
        if interfaces is None:
            interfaces = []
        elif isinstance(interfaces, (list, tuple)):
            pass
        elif isinstance(interfaces, str):
            interfaces = [str]
        self._ifaces = interfaces
        self._wifi_scan_timer = None

    def start_collecting(self):
        """Start collecting."""
        self._wifi_scan_timer = self.start_timer(self._scan_interval,
                                                 self._wifi_scan)

    def stop_collecting(self):
        """Stop collecting."""
        if self._wifi_scan_timer is not None:
            self.cancel_timer(self._wifi_scan_timer)

    def _wifi_scan(self):
        for interface in self._ifaces:
            # if has wildcard, deal with it
            result = Cell.all(self._iface_name)

        return True


_DOMAINS = {'wifi': WifiDomain}
