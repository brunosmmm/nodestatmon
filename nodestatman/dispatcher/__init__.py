"""Dispatcher."""


class Dispatcher:
    """Dispatcher."""

    def __init__(self, controller, **kwargs):
        """Initialize."""
        self._controller = controller

    def start_dispatching(self):
        """Start dispatching."""
        pass

    def stop_dispatching(self):
        """Stop dispatching."""
        pass

    def dispatch_commit(self, domain, instance, field, value):
        """Dispatch commited value."""
        raise NotImplementedError
