from ._transport import Transport
from ._server_sent_events import ServerSentEventsTransport
from ._web_sockets import WebSocketsTransport
from ._url import get_url

available_transports = {
    WebSocketsTransport.name: WebSocketsTransport,
    ServerSentEventsTransport.name: ServerSentEventsTransport
}


