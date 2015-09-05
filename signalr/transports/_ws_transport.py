import json
import urlparse

from websocket import create_connection
from ._transport import Transport


class WebSocketsTransport(Transport):
    def __init__(self, session, event_handlers):
        Transport.__init__(self, session, event_handlers)
        self.ws = None

    def _get_name(self):
        return 'webSockets'

    def _get_transport_specific_url(self, url):
        parsed = urlparse.urlparse(url)
        scheme = 'wss' if parsed.scheme == 'https' else 'ws'
        url_data = (scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)

        return urlparse.urlunparse(url_data)

    def start(self, connection):
        self.ws = create_connection(self._get_url(connection, 'connect'),
                                    header=self.__get_headers(),
                                    cookie=self.__get_cookie_str())

        def _receive():
            while True:
                notification = self.ws.recv()
                self._handle_notification(notification)

        return _receive

    def send(self, connection, data):
        self.ws.send(json.dumps(data))

    def close(self, connection):
        self.ws.close()

    def accept(self, negotiate_data):
        return bool(negotiate_data['TryWebSockets'])

    def __get_headers(self):
        headers = self._session.headers

        return map(lambda name: '{name}: {value}'.format(name=name, value=headers[name]), headers)

    def __get_cookie_str(self):
        return '; '.join(
            map(lambda (name, value): '{name}={value}'.format(name=name, value=value),
                self._session.cookies.iteritems()))
