signalr-client-py
=================

Python client proxy for `SignalR <http://signalr.net/>`_.


Requirements
------------

Install requirements by running::

    pip install -r requirements


Signalr client is based on `gevent` which in turn requires Python headers.
In Debian based distributions (such as Ubuntu and Raspbian) they are called `python-dev`.


Compatibility
-------------

Compatible with Python 2 and 3.


Usage
-----
Here is sample usage::

    from requests import Session
    from signalr import Connection

    with Session() as session:
        #create a connection
        connection = Connection("http://localhost:5000/signalr", session)

        #get chat hub
        chat = connection.register_hub('chat')

        #start a connection
        connection.start()

        #create new chat message handler
        def print_received_message(data):
            print('received: ', data)

        #create new chat topic handler
        def print_topic(topic, user):
            print('topic: ', topic, user)

        #create error handler
        def print_error(error):
            print('error: ', error)

        #receive new chat messages from the hub
        chat.client.on('newMessageReceived', print_received_message)

        #change chat topic
        chat.client.on('topicChanged', print_topic)

        #process errors
        connection.error += print_error

        #start connection, optionally can be connection.start()
        with connection:

            #post new message
            chat.server.invoke('send', 'Python is here')

            #change chat topic
            chat.server.invoke('setTopic', 'Welcome python!')

            #invoke server method that throws error
            chat.server.invoke('requestError')

            #post another message
            chat.server.invoke('send', 'Bye-bye!')

            #wait a second before exit
            connection.wait(1)

