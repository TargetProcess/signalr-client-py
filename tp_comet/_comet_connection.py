from requests import Session
from signalr import Connection


class CometConnection:
    def __init__(self, url, username, password, **kwargs):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__session = kwargs.get('session', Session())
        self.__session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        self.__connection = Connection('{url}/notifications'.format(url=url), self.__session)
        self.__hubs = dict([
            self.__create_hub('slice'),
            self.__create_hub('resource'),
            self.__create_hub('entitytreeviewslice'),
            self.__create_hub('timelineslice'),
            self.__create_hub('treeviewslice'),
            self.__create_hub('viewmenu')
        ])

    def start(self):
        self.__login()
        self.__connection.start()

    def __login(self):
        self.__session.post('{url}/login.aspx'.format(url=self.__url), data={
            "scriptManager": 'mainPanel|btnLogin',
            "UserName": self.__username,
            "Password": self.__password,
            "__EVENTTARGET": '',
            "__EVENTARGUMENT": '',
            "btnLogin": 'Log in'
        }, headers={
            "X-Requested-With": "XMLHttpRequest",
            "Cache-Control": "no-cache",
            "X-MicrosoftAjax": "Delta=true",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })

    def __create_hub(self, hub_name):
        return hub_name, CometHub(self.__connection.hub(hub_name))

    def get(self, hub_name):
        return self.__hubs[hub_name]


class CometHub:
    def __init__(self, hub):
        self.__hub = hub

    def subscribe(self, subscription, callback):
        self.__hub.client.on('notifyChanged', callback)
        self.__hub.server.invoke('Subscribe', subscription)

    def unsubscribe(self, subscription_id):
        self.__hub.server.invoke('Unsubscribe', subscription_id)
