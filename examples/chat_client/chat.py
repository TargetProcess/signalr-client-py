from requests import Session
from requests.auth import HTTPBasicAuth
from signalr import Connection

with Session() as session:
    session.auth = HTTPBasicAuth("known", "user")
    connection = Connection("http://localhost:5000/signalr", session)
    chat = connection.register_hub('chat')


    def print_received_message(data):
        print('received: ', data)


    def print_topic(topic, user):
        print('topic: ', topic, user)


    def print_error(error):
        print('error: ', error)


    chat.client.on('newMessageReceived', print_received_message)
    chat.client.on('topicChanged', print_topic)

    connection.error += print_error

    with connection:
        chat.server.invoke('send', 'Python is here')
        chat.server.invoke('setTopic', 'Welcome python!')
        chat.server.invoke('requestError')
        chat.server.invoke('send', 'Bye-bye!')

        connection.wait(1)
