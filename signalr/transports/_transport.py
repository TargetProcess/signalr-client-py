from abc import abstractmethod
import json

from ._events import EventHook


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
