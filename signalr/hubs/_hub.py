from signalr.events import EventHook


class Hub:
    def __init__(self, name, connection):
        self.server = HubServer(name, connection)
        self.client = HubClient(name, connection)


class HubServer:
    def __init__(self, name, connection):
        self.name = name
        self.__connection = connection

    def invoke(self, method, data):
        self.__connection.send({
            'H': self.name,
            'M': method,
            'A': [data],
            'I': self.__connection.increment_send_counter()
        })


class HubClient(object):
    def __init__(self, name, connection):
        self.name = name
        self.__handlers = {}

        def handle(data):
            inner_data = data['M'][0] if 'M' in data and len(data['M']) > 0 else {}
            hub = inner_data['H'] if 'H' in inner_data else ''
            if hub.lower() == self.name.lower():
                method = inner_data['M']
                if method in self.__handlers:
                    arguments = inner_data['A']
                    self.__handlers[method].fire(data=arguments)

        connection.subscribe(handle)

    def on(self, method, handler):
        if method not in self.__handlers:
            self.__handlers[method] = EventHook()
        self.__handlers[method] += handler

    def off(self, method, handler):
        if method in self.__handlers:
            self.__handlers[method] -= handler
