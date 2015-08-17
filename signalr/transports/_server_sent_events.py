import json
import urllib

import requests
import sseclient

from signalr.transports import Transport


class ServerSentEventsTransport(Transport):
    def __init__(self, url, cookies, connection_token):
        Transport.__init__(self, url, cookies, connection_token)
        user_agent = str.split(self._user_agent_header, ': ')
        self.headers = {
            user_agent[0]: user_agent[1],
            'Cookie': self._get_auth_cookie()
        }

    def send(self, data):
        requests.post(self.__get_send_url(), cookies=self._cookies, headers=self.headers,
                      data={'data': json.dumps(data)})

    def start(self):
        notifications = sseclient.SSEClient(self.__get_sse_url(), headers=self.headers)

        def _receive():
            for notification in notifications:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive

    def __get_sse_url(self):
        return '{url}/connect?transport=serverSentEvents&connectionToken={connection_token}'.format(url=self._url,
                                                                                                    connection_token=urllib.quote_plus(
                                                                                                        self._connection_token))

    def __get_send_url(self):
        return '{url}/send?transport=serverSentEvents&connectionToken={connection_token}'.format(url=self._url,
                                                                                                 connection_token=urllib.quote_plus(
                                                                                                     self._connection_token))
