""""Nodestatman."""

from threading import Thread
import time


class Controller(Thread):
    """Controller."""

    def __init__(self, domains, domain_configurations, **kwargs):
        """Initialize."""
        super().__init__(**kwargs)
        self._domains = {}
        for domain_name, domain_class in domains.items():
            domain_configuration = domain_configurations[domain_name]
            ret = self._initialize_domain(domain_name,
                                          domain_class,
                                          domain_configuration)

    def _initialize_domain(self, domain_name, domain_class, configuration):
        """Initialize domain."""

        if domain_name in self._domains:
            # log error, already loaded
            return False

        try:
            domain = domain_class(self, **configuration)
        except Exception as ex:
            # log some stuff
            return False

        # save object
        self._domains[domain_name] = domain

        return True

    def request_timer(self, domain, timeout, callback):
        """Request timer."""
        pass

    def run(self):
        while True:
            time.sleep(0.1)
