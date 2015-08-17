import json

import gevent
import requests

import transports

_available_transports = {
    'webSockets': transports.WebSocketsTransport,
    'serverSentEvents': transports.ServerSentEventsTransport
}

_hub_send_counter = -1


class Connection:
    def __init__(self, url, cookies):
        self.__cookies = cookies
        self.__url = url
        self.__transport = None
        self.__hubs = {}

    def __get_transport(self, negotiate_data):
        try_web_sockets = bool(negotiate_data['TryWebSockets'])
        ctor = _available_transports['webSockets'] if try_web_sockets else _available_transports['serverSentEvents']
        connection_token = negotiate_data['ConnectionToken']

        return ctor(self.__url, self.__cookies, connection_token)

    def start(self):
        negotiate = requests.get('{0}/negotiate'.format(self.__url), cookies=self.__cookies)
        negotiate_data = json.loads(negotiate.content)
        transport = self.__get_transport(negotiate_data)
        listener = transport.start()
        gevent.spawn(listener)

        self.__transport = transport

    def subscribe(self, handler):
        self.__transport.handlers += handler

    def unsubscribe(self, handler):
        self.__transport.handlers -= handler

    def send(self, data):
        self.__transport.send(data)

    def hub(self, name):
        if name not in self.__hubs:
            self.__hubs[name] = Hub(name, self)
        return self.__hubs[name]


class Hub:
    def __init__(self, name, connection):
        self.server = HubServer(name, connection)
        self.client = HubClient(name, connection)


class HubServer:
    def __init__(self, name, connection):
        self.name = name
        self.__connection = connection

    def invoke(self, method, data):
        self.__connection.send({
            'H': self.name,
            'M': method,
            'A': [data],
            'I': ++_hub_send_counter
        })

    def __getattr__(self, method):
        def _missing(data):
            self.invoke(method, data)

        return _missing


class HubClient(object):
    def __init__(self, name, connection):
        self.name = name
        self.__connection = connection

        def handle(data):
            if 'M' in data and 'H' in data['M'] and data['M']['H'] == self.name:
                getattr(self, data['M']['M'])(data['M']['A'])

        self.__connection.subscribe(handle)
