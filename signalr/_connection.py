import json

import gevent
import requests
from signalr.hubs import Hub
from signalr.transports import get_url, get_transport


class Connection:
    def __init__(self, url, cookies):
        self.__cookies = cookies
        self.__url = url
        self.__hubs = {}
        self.hub_send_counter = 0

        url = get_url(self.__url, 'negotiate')
        negotiate = requests.get(url, cookies=self.__cookies)
        negotiate_data = json.loads(negotiate.content)
        transport = self.__get_transport(negotiate_data)
        self.__transport = transport

    def __get_transport(self, negotiate_data):
        return get_transport(negotiate_data, self.__url, self.__cookies)

    def __get_connection_data(self):
        return json.dumps(map(lambda hub_name: {'name': hub_name}, self.__hubs))

    def start(self):
        listener = self.__transport.start(self.__get_connection_data())
        gevent.spawn(listener)

    def subscribe(self, handler):
        self.__transport.handlers += handler

    def unsubscribe(self, handler):
        self.__transport.handlers -= handler

    def send(self, data):
        self.__transport.send(data, self.__get_connection_data())

    def hub(self, name):
        if name not in self.__hubs:
            self.__hubs[name] = Hub(name, self)
        return self.__hubs[name]
