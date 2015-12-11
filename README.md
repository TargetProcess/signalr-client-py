# signalr-client-py

Python client proxy for [SignalR](http://signalr.net/).

## Requirements

Install the following prerequisites using `pip`:

* `gevent`
* `sseclient`
* `websocket-client`

The `gevent` package in turn requires Python headers.
In Debian based distributions (such as Ubuntu and Raspbian) they are called `python-dev`.

## Compatibility

Compatible with Python 2 and 3.

For Python 3, you need to install a version of `gevent` >= 1.1rc1.

## Usage

```
#create a connection
connection = Connection(url, session)

#start a connection
connection.start()

#add a handler to process notifications to the connection 
connection.handlers += lambda data: print 'Connection: new notification.', data

#get chat hub
chat_hub = connection.hub('chat')

#create new chat message handler
def message_received(message):
   print 'Hub: New message.', message
   
#receive new chat messages from the hub
chat_hub.client.on('message_received', message_received)

#send a new message to the hub
chat_hub.server.invoke('send_message', 'Hello!')

#do not receive new messages
chat_hub.client.off('message_received', message_received)

#close the connection
connection.close()
```
