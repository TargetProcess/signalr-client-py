import json
import gevent
from signalr.events import EventHook
from signalr.hubs import Hub
from signalr.transports import AutoTransport


class Connection:
    protocol_version = '1.5'

    def __init__(self, url, session):
        self.url = url
        self.__hubs = {}
        self.__send_counter = -1
        self.connection_token = None
        self.connection_data = None
        self.handlers = EventHook()
        self.__transport = AutoTransport(session, self.handlers)
        self.__greenlet = None

    def __get_connection_data(self):
        return json.dumps([{'name': hub_name} for hub_name in self.__hubs])

    def increment_send_counter(self):
        self.__send_counter += 1
        return self.__send_counter

    def start(self):
        self.connection_data = self.__get_connection_data()
        negotiate_data = self.__transport.negotiate(self)
        self.connection_token = negotiate_data['ConnectionToken']

        listener = self.__transport.start(self)

        def wrapped_listener():
            listener()
            gevent.sleep(0)

        self.__greenlet = gevent.spawn(wrapped_listener)

    def wait(self, timeout=30):
        gevent.joinall([self.__greenlet], timeout)

    def send(self, data):
        self.__transport.send(self, data)

    def close(self):
        gevent.kill(self.__greenlet)
        self.__transport.close(self)

    def hub(self, name):
        if name not in self.__hubs:
            self.__hubs[name] = Hub(name, self)
            self.connection_data = self.__get_connection_data()
        return self.__hubs[name]

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
