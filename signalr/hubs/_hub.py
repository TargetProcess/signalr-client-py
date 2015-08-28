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

    def __getattr__(self, method):
        def _missing(data):
            self.invoke(method, data)

        return _missing


class HubClient(object):
    def __init__(self, name, connection):
        self.name = name
        self.__connection = connection

        def handle(data):
            inner_data = data['M'][0] if 'M' in data and len(data['M']) > 0 else {}
            hub = inner_data['H'] if 'H' in inner_data else ''
            if hub == self.name:
                method = inner_data['M']
                arguments = inner_data['A']
                getattr(self, method)(arguments)

        self.__connection.subscribe(handle)
