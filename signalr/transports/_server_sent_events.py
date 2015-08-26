import json
import urllib

import requests
import sseclient

from signalr.transports import Transport


class ServerSentEventsTransport(Transport):
    def __init__(self, url, cookies, connection_token, connection_data):
        Transport.__init__(self, url, cookies, connection_token, connection_data)

    def send(self, data):
        requests.post(self.__get_send_url(), headers=self._headers,
                      data={'data': json.dumps(data)})

    def start(self):
        notifications = sseclient.SSEClient(self.__get_sse_url(), headers=self._headers)
        requests.get(self.__get_start_url(), headers=self._headers)

        def _receive():
            for notification in notifications:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive

    def __get_sse_url(self):
        return self.__get_url('connect')

    def __get_send_url(self):
        return self.__get_url('send')

    def __get_start_url(self):
        return self.__get_url('start')

    def __get_url(self, action):
        return '{url}/{action}?transport=serverSentEvents&clientProtocol=1.5&connectionToken={connection_token}&connectionData={connection_data}'.format(
            url=self._url, action=action, connection_token=urllib.quote_plus(self._connection_token),
            connection_data=self._connection_data)
