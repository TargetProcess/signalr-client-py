from abc import abstractmethod
import json
import urllib


class Transport:
    def __init__(self, session, event_handlers):
        self._session = session
        self.__handlers = event_handlers

    @abstractmethod
    def _get_name(self):
        pass

    def negotiate(self, connection):
        url = self.__get_base_url(connection.url, connection, 'negotiate', connectionData=connection.connection_data)
        negotiate = self._session.get(url)

        return json.loads(negotiate.content)

    @abstractmethod
    def start(self, connection):
        pass

    @abstractmethod
    def send(self, connection, data):
        pass

    @abstractmethod
    def close(self, connection):
        pass

    def accept(self, negotiate_data):
        return True

    def _handle_notification(self, message):
        if len(message) == 0:
            return

        data = json.loads(message)
        self.__handlers.fire(data=data)

    def _get_url(self, connection, action, **kwargs):
        args = kwargs.copy()
        args['transport'] = self._get_name()
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
