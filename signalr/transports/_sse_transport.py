import json
import sseclient
from ._transport import Transport


class ServerSentEventsTransport(Transport):
    def __init__(self, session):
        Transport.__init__(self, session)

    def _get_name(self):
        return 'serverSentEvents'

    def send(self, connection, data):
        self._session.post(self._get_url(connection, 'send'), data={'data': json.dumps(data)})

    def start(self, connection):
        notifications = sseclient.SSEClient(self._get_url(connection, 'connect'), session=self._session)
        self._session.get(self._get_url(connection, 'start'))

        def _receive():
            for notification in notifications:
                if notification.data != 'initialized':
                    self._handle_notification(notification.data)

        return _receive
