from ._transport import Transport
from ._sse_transport import ServerSentEventsTransport
from ._ws_transport import WebSocketsTransport


class AutoTransport(Transport):
    def __init__(self, session, event_handlers):
        Transport.__init__(self, session, event_handlers)
        self.__available_transports = [
            WebSocketsTransport(session, event_handlers),
            ServerSentEventsTransport(session, event_handlers)
        ]
        self.__transport = None

    def negotiate(self, connection):
        negotiate_data = Transport.negotiate(self, connection)
        self.__transport = self.__get_transport(negotiate_data)

        return negotiate_data

    def __get_transport(self, negotiate_data):
        for transport in self.__available_transports:
            if transport.accept(negotiate_data):
                return transport
        raise Exception('Cannot find suitable transport')

    def start(self, connection):
        return self.__transport.start(connection)

    def send(self, connection, data):
        self.__transport.send(connection, data)

    def close(self, connection):
        self.__transport.close(connection)

    def _get_name(self):
        return 'auto'
