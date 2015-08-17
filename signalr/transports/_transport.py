from abc import abstractmethod
import json

import requests

from ._events import EventHook


class Transport:
    _user_agent_header = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

    def __init__(self, url, cookies, connection_token):
        self._connection_token = connection_token
        self._cookies = cookies
        self._url = url
        self.handlers = EventHook()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send(self, data):
        pass

    def _get_auth_cookie(self):
        return ".ASPXAUTH={0}".format(requests.utils.dict_from_cookiejar(self._cookies).get(".ASPXAUTH"))

    def _handle_notification(self, message):
        if len(message) == 0:
            return

        data = json.loads(message)
        self.handlers.fire(data=data)
