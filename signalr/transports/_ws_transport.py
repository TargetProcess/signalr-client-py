import json
import urlparse

from websocket import create_connection

from ._transport import Transport


def accept_ws(negotiate_data):
    return bool(negotiate_data['TryWebSockets'])


class WebSocketsTransport(Transport):
    def __init__(self, cookies):
        Transport.__init__(self, cookies)
        self.ws = None

    def _get_transport_name(self):
        return 'webSockets'

    def _get_transport_specific_url(self, url):
        parsed = urlparse.urlparse(url)
        scheme = 'wss' if parsed.scheme == 'https' else 'ws'
        url_data = (scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)

        return urlparse.urlunparse(url_data)

    def start(self, connection):
        self.ws = create_connection(self._get_url(connection, 'connect'), header=self.__get_headers())

        def _receive():
            while True:
                notification = self.ws.recv()
                self._handle_notification(notification)

        return _receive

    def __get_headers(self):
        return map(lambda name: '{name}: {value}'.format(name=name, value=self._headers[name]), self._headers)

    def send(self, connection, data):
        self.ws.send(json.dumps(data))
