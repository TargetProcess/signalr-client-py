import json

import requests
import sseclient

from ._transport import Transport


def accept_sse(negotiate_data):
    return True


class ServerSentEventsTransport(Transport):
    name = 'serverSentEvents'

    def __init__(self, url, cookies, connection_token):
        Transport.__init__(self, url, cookies, connection_token)

    def _get_transport_name(self):
        return ServerSentEventsTransport.name

    def send(self, data, connection_data):
        requests.post(self._get_url('send', connectionData=connection_data), headers=self._headers,
                      data={'data': json.dumps(data)})

    def start(self, connection_data):
        notifications = sseclient.SSEClient(self._get_url('connect', connectionData=connection_data), headers=self._headers)
        requests.get(self._get_url('start', connectionData=connection_data), headers=self._headers)

        def _receive():
            for notification in notifications:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive
