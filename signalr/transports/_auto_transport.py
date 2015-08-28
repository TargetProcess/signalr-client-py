from ._transport import Transport
from ._sse_transport import accept_sse, ServerSentEventsTransport
from ._ws_transport import accept_ws, WebSocketsTransport


class AutoTransport(Transport):
    name = 'auto'

    def __init__(self, cookies):
        Transport.__init__(self, cookies)
        self.__available_transports = [
            (accept_ws, WebSocketsTransport(cookies)),
            (accept_sse, ServerSentEventsTransport(cookies))
        ]
        self.__transport = None

    def negotiate(self, connection):
        negotiate_data = Transport.negotiate(self, connection)
        self.__transport = self.__get_transport(negotiate_data)

        return negotiate_data

    def __get_transport(self, negotiate_data):
        for (accept, transport) in self.__available_transports:
            if accept is None or accept(negotiate_data):
                return transport
        raise Exception('Cannot find suitable transport')

    def start(self, connection):
        return self.__transport.start(connection)

    def send(self, connection, data):
        self.__transport.send(connection, data)

    def _get_transport_name(self):
        return AutoTransport.name
