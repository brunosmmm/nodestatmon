"""Controller."""

from threading import Thread, Event
from collections import namedtuple, deque
import datetime
import shortuuid
import time
import logging


class ControllerTimer:
    """Timer object."""

    def __init__(self, uuid, domain, period, timeout, callback):
        """Initialize."""
        self.uuid = uuid
        self.domain = domain
        self.period = period
        self.timeout = timeout
        self.callback = callback


class Controller(Thread):
    """Controller."""

    def __init__(self, domains, domain_configurations, dispatchers,
                 dispatcher_configurations, **kwargs):
        """Initialize."""
        super().__init__(**kwargs)
        self._stop_controller = Event()
        self._domains = {}
        self._dispatchers = {}
        self._timers = {}
        self._timers_to_cancel = deque()
        self._logger = logging.getLogger('statman.controller')
        # create dispatchers
        for dispatcher_name, dispatcher_class in dispatchers.items():
            dispatcher_configuration = dispatcher_configurations[dispatcher_name]
            ret = self._initialize_dispatcher(dispatcher_name,
                                              dispatcher_class,
                                              dispatcher_configuration)
        # create domains
        for domain_name, domain_class in domains.items():
            domain_configuration = domain_configurations[domain_name]
            ret = self._initialize_domain(domain_name,
                                          domain_class,
                                          domain_configuration)

    def _initialize_dispatcher(self, dispatcher_name, dispatcher_class,
                               configuration):
        try:
            dispatcher = dispatcher_class(self, **configuration)
            self._logger.info('initialized dispatcher {}'
                              .format(dispatcher_name))
        except Exception as ex:
            print(ex)
            return False

        self._dispatchers[dispatcher_name] = dispatcher

        return True

    def _initialize_domain(self, domain_name, domain_class, configuration):
        """Initialize domain."""

        if domain_name in self._domains:
            # log error, already loaded
            return False

        try:
            domain = domain_class(self, **configuration)
            self._logger.info('initialized domain {}'.format(domain_name))
        except Exception as ex:
            # log some stuff
            return False

        # save object
        self._domains[domain_name] = domain

        return True

    def _request_timer(self, domain, timeout, callback):
        """Request timer."""
        timer_uuid = shortuuid.uuid()
        self._timers[timer_uuid] = ControllerTimer(timer_uuid,
                                                   domain,
                                                   timeout,
                                                   datetime.datetime.now() +
                                                   datetime.timedelta(seconds=timeout),
                                                   callback)
        return timer_uuid

    def _commit(self, domain, instance_name, field_name, value):
        """Commit value."""
        for dispatcher_name, dispatcher in self._dispatchers.items():
            dispatcher.dispatch_commit(domain, instance_name, field_name,
                                       value)

    def cancel_timer(self, timer_uuid):
        """Cancel timer."""
        self._timers_to_cancel.appendleft(timer_uuid)

    def stop_controller(self):
        """Stop controller."""
        for domain in self._domains.values():
            domain.stop_collecting()
        for dispatcher in self._dispatchers.values():
            dispatcher.stop_dispatching()
        self._stop_controller.set()
        self.join()
        self._logger.info('controller stoped')

    def start_controller(self):
        for dispatcher in self._dispatchers.values():
            dispatcher.start_dispatching()
        for domain in self._domains.values():
            domain.start_collecting()
        self.start()
        self._logger.info('controller started')

    def run(self):
        while not self._stop_controller.is_set():
            now = datetime.datetime.now()
            expired_timers = []
            if len(self._timers_to_cancel) > 0:
                cancel_uuid = self._timers_to_cancel.pop()
                if cancel_uuid in self._timers:
                    del self._timers[cancel_uuid]
            for timer_uuid, timer in self._timers.items():
                td = timer.timeout - now
                if td.seconds > 0:
                    # not expired
                    continue

                # expired
                restart = False
                if timer.callback is not None:
                    restart = timer.callback()

                if restart is False:
                    self._logger.debug('marking timer {} for removal'
                                       .format(timer_uuid))
                    expired_timers.append(timer_uuid)
                else:
                    timer.timeout = now + datetime.timedelta(
                        seconds=timer.period)

            for timer in expired_timers:
                del self._timers[timer]

            time.sleep(1)
