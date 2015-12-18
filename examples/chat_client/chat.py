from requests import Session
from requests.auth import HTTPBasicAuth
from gevent import monkey

monkey.patch_socket()

from signalr import Connection

with Session() as session:
    connection = Connection("http://localhost:5000/signalr", session)
    chat = connection.hub('chat')


    def print_data(data, timestamp):
        print(data, timestamp)


    def print_topic(topic):
        print(topic)


    chat.client.on('newMessageReceived', print_data)
    chat.client.on('topicChanged', print_topic)

    with connection:
        send = chat.server.invoke('send', 'Python is here')
        set_topic = chat.server.invoke('setTopic', 'Python!')

        session.auth = HTTPBasicAuth("known", "user")
        chat.server.invoke('setTopic', 'No anonymity any more')

        connection.wait(5)

        chat.server.invoke('send', 'Shutting down')

        connection.wait(2)
