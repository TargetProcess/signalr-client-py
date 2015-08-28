import json

import gevent

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
        self.__transport = AutoTransport(session)

    def __get_connection_data(self):
        return json.dumps(map(lambda hub_name: {'name': hub_name}, self.__hubs))

    def increment_send_counter(self):
        self.__send_counter += 1
        return self.__send_counter

    def start(self):
        self.connection_data = self.__get_connection_data()
        negotiate_data = self.__transport.negotiate(self)
        self.connection_token = negotiate_data['ConnectionToken']

        listener = self.__transport.start(self)
        gevent.spawn(listener)

    def subscribe(self, handler):
        self.__transport.handlers += handler

    def unsubscribe(self, handler):
        self.__transport.handlers -= handler

    def send(self, data):
        self.__transport.send(self, data)

    def hub(self, name):
        if name not in self.__hubs:
            self.__hubs[name] = Hub(name, self)
            self.connection_data = self.__get_connection_data()
        return self.__hubs[name]
