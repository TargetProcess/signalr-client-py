from abc import abstractmethod
import json
import urllib
import requests

from ._events import EventHook


class Transport:
    def __init__(self, cookies):
        self._cookies = cookies
        self._connection_token = None
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

    def negotiate(self, connection):
        url = self.__get_base_url(connection.url, connection, 'negotiate', connectionData=connection.connection_data)
        negotiate = requests.get(url, headers=self._headers)

        return json.loads(negotiate.content)

    @abstractmethod
    def start(self, connection):
        pass

    @abstractmethod
    def send(self, connection, data):
        pass

    def _handle_notification(self, message):
        print message
        if len(message) == 0:
            return

        data = json.loads(message)
        self.handlers.fire(data=data)

    def _get_url(self, connection, action, **kwargs):
        args = kwargs.copy()
        args['transport'] = self._get_transport_name()
        args['connectionToken'] = connection.connection_token
        args['connectionData'] = connection.connection_data

        url = self._get_transport_specific_url(connection.url)
        return self.__get_base_url(url, connection, action, **args)

    def _get_transport_specific_url(self, url):
        return url

    @staticmethod
    def __get_base_url(url, connection, action, **kwargs):
        args = kwargs.copy()
        args['clientProtocol'] = connection.protocol_version
        query = '&'.join(map(lambda key: '{key}={value}'.format(key=key, value=urllib.quote_plus(args[key])), args))

        return '{url}/{action}?{query}'.format(url=url,
                                               action=action,
                                               query=query)
