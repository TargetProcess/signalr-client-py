import json

import requests
import sseclient

from ._transport import Transport


def accept_sse(negotiate_data):
    return True


class ServerSentEventsTransport(Transport):
    def __init__(self, cookies):
        Transport.__init__(self, cookies)

    def _get_transport_name(self):
        return 'serverSentEvents'

    def send(self, connection, data):
        requests.post(self._get_url(connection, 'send'), headers=self._headers, data={'data': json.dumps(data)})

    def start(self, connection):
        notifications = sseclient.SSEClient(self._get_url(connection, 'connect'), headers=self._headers)
        requests.get(self._get_url(connection, 'start'), headers=self._headers)
        print 'started'

        def _receive():
            for notification in notifications:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive
