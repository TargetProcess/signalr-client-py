import json
import urllib
import urlparse

from websocket import create_connection

from signalr.transports import Transport


class WebSocketsTransport(Transport):
    def __init__(self, url, cookies, connection_token, connection_data):
        Transport.__init__(self, url, cookies, connection_token)
        self.ws = None

        parsed = urlparse.urlparse(url)
        self._url = '{scheme}://{url.hostname}{url.path}/connect?transport=webSockets&connectionToken={connection_token}&connectionData={connection_data}&clientProtocol=1.5'.format(
            scheme=('ws' if parsed.scheme == 'http' else 'wss'),
            url=parsed,
            connection_token=urllib.quote_plus(self._connection_token),
            connection_data=urllib.quote_plus(json.dumps(connection_data)))

    def start(self):
        self.ws = create_connection(self._url,
                                    None,
                                    cookie=self._get_auth_cookie(),
                                    header=[self._user_agent_header])

        def _receive():
            while True:
                notification = self.ws.recv()
                self._handle_notification(notification)

        return _receive

    def send(self, data):
        self.ws.send(json.dumps(data))
