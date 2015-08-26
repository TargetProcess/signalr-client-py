import json

import requests
import sseclient

from signalr.transports import Transport


class ServerSentEventsTransport(Transport):
    name = 'serverSentEvents'

    def __init__(self, url, cookies, connection_token, connection_data):
        Transport.__init__(self, url, cookies, connection_token, connection_data)

    def _get_transport_name(self):
        return ServerSentEventsTransport.name

    def send(self, data):
        requests.post(self._get_url('send'), headers=self._headers,
                      data={'data': json.dumps(data)})

    def start(self):
        notifications = sseclient.SSEClient(self._get_url('connect'), headers=self._headers)
        requests.get(self._get_url('start'), headers=self._headers)

        def _receive():
            for notification in notifications:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive
