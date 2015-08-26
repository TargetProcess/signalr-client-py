from ._server_sent_events import ServerSentEventsTransport, accept_sse
from ._web_sockets import WebSocketsTransport, accept_ws

_available_transports = {
    WebSocketsTransport.name: (accept_ws, WebSocketsTransport),
    ServerSentEventsTransport.name: (accept_sse, ServerSentEventsTransport)
}


def get_transport(negotiate_data, url, cookie, connection_data):
    for transport in _available_transports:
        (accept, transport_ctor) = _available_transports[transport]
        if accept is None or accept(negotiate_data):
            connection_token = negotiate_data['ConnectionToken']
            return transport_ctor(url, cookie, connection_token, connection_data)
    raise Exception('Cannot find suitable transport')
