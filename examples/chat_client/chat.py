from requests import Session
from requests.auth import HTTPBasicAuth
from signalr import Connection

with Session() as session:
    connection = Connection("http://localhost:5000/signalr", session)
    chat = connection.register_hub('chat')


    def print_received_message(data, timestamp):
        print('received: ', data, timestamp)


    def print_topic(topic):
        print('topic: ', topic)


    def print_error(error):
        print('error: ', error)


    chat.client.on('newMessageReceived', print_received_message)
    chat.client.on('topicChanged', print_topic)

    chat.error += print_error

    with connection:
        chat.server.invoke('send', 'Python is here')
        chat.server.invoke('setTopic', 'Topic from python client')

        session.auth = HTTPBasicAuth("known", "user")
        chat.server.invoke('setTopic', 'Topic is set by known user')

        connection.wait(5)

        chat.server.invoke('send', 'Bye-bye!')

        connection.wait(2)
