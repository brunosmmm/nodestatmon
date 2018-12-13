"""Domains."""

import os
import importlib.util


class Domain:
    """Abstract domain class."""

    def __init__(self, controller, **kwargs):
        """Initialize."""
        self._controller = controller

    def start_collecting(self):
        """Start collecting."""
        raise NotImplementedError

    def stop_collecting(self):
        """Stop collecting."""
        raise NotImplementedError

    def timer_start(self, timeout, callback):
        """Start a timer."""
        return self._controller._request_timer(self._DOMAIN, timeout, callback)

    def timer_cancel(self, timer_uuid):
        """Cancel a timer."""
        self._controller.cancel_timer(timer_uuid)

    def register_instance(self, instance_name):
        """Register an instance."""
        pass

    def register_field(self, field_name):
        """Register field name."""
        pass

    def commit_reading(self, instance_name, field_name, value):
        """Commit a reading."""
        self._controller._commit(self._DOMAIN, instance_name, field_name, value)



def load_domains(path):
    if not os.path.isdir(path):
        raise OSError('path is not a directory')

    loaded_domains = {}
    for f in os.listdir(path):
        if not os.path.isfile(os.path.join(path, f)):
            continue

        base, ext = os.path.splitext(os.path.join(path, f))
        if ext != '.py':
            continue
        if base == '__init__':
            continue

        domains = load_domain(base, os.path.join(path, f))
        loaded_domains.update(domains)

    return loaded_domains


def load_domain(name, path):
    # load module
    full_path = os.path.join(os.getcwd(), path)
    spec = importlib.util.spec_from_file_location(name, full_path)
    _module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_module)

    if not hasattr(_module, '_DOMAINS'):
        return {}

    return _module._DOMAINS
