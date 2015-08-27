from ._server_sent_events import ServerSentEventsTransport, accept_sse
from ._web_sockets import WebSocketsTransport, accept_ws

_available_transports = {
    WebSocketsTransport.name: (accept_ws, WebSocketsTransport),
    ServerSentEventsTransport.name: (accept_sse, ServerSentEventsTransport)
}


def get_transport(negotiate_data, url, cookie):
    for transport in _available_transports:
        (accept, transport_ctor) = _available_transports[transport]
        if accept is None or accept(negotiate_data):
            return transport_ctor(url, cookie, negotiate_data['ConnectionToken'])
    raise Exception('Cannot find suitable transport')
