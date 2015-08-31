import json
import sseclient
from ._transport import Transport


class ServerSentEventsTransport(Transport):
    def __init__(self, session, event_handlers):
        Transport.__init__(self, session, event_handlers)
        self.__response = None

    def _get_name(self):
        return 'serverSentEvents'

    def start(self, connection):
        self.__response = sseclient.SSEClient(self._get_url(connection, 'connect'), session=self._session)
        self._session.get(self._get_url(connection, 'start'))

        def _receive():
            for notification in self.__response:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive

    def send(self, connection, data):
        self._session.post(self._get_url(connection, 'send'), data={'data': json.dumps(data)})

    def close(self):
        self.__response.resp.close()
