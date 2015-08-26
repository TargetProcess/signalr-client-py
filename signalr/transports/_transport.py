from abc import abstractmethod
import json

from ._events import EventHook
from ._url import get_url


class Transport:
    def __init__(self, url, cookies, connection_token, connection_data):
        self._connection_token = connection_token
        self._url = url
        self._connection_data = connection_data
        self.handlers = EventHook()
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Cookie': self.__get_cookie_str(cookies)
        }

    @abstractmethod
    def _get_transport_name(self):
        pass

    @staticmethod
    def __get_cookie_str(cookies):
        return '; '.join(
            map(lambda (name, value): '{name}={value}'.format(name=name, value=value), cookies.iteritems()))

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send(self, data):
        pass

    def _handle_notification(self, message):
        if len(message) == 0:
            return

        data = json.loads(message)
        self.handlers.fire(data=data)

    def _get_url(self, action, **kwargs):
        args = kwargs.copy()
        args['transport'] = self._get_transport_name()
        args['connectionToken'] = self._connection_token
        args['connectionData'] = self._connection_data

        return get_url(self._url, action, **args)

    def __get_url(self, action):
        return self._get_url(action, self._get_transport_name())
