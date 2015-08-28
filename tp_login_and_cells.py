import urlparse

from locust import HttpLocust, TaskSet, task, events
from locust.events import request_success
from statsd import StatsClient
import signalr


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        self.login()
        self.definition = self.get_slice_definition()
        self.subscribe_to_slice_notifications()

    def login(self):
        self.client.post("/login.aspx", data={
            "scriptManager": "mainPanel|btnLogin",
            "UserName": "admin",
            "Password": "admin",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": "ocOVcgQ8LYR1uNc2jPh+UeFStpaCqw97OFABoDapMR9KTH8BGeDWwDbw9vNG+FWsZanZSoS2rnV95g04VqiDbvkvibKczw4HhcguVcjT9qRWYGEJory4y8bB4+jom/5lCsTnqZ2LxakpHc2zFnFkZn8t378WcapgP4aW3sSFXnN40l4xMU5qnmLmnyXLXakWGD0LlyI1CHDgxhu54n6uwzT7O9hnESf/WcLMjnv4Av0t54BMzktPFkhI+XOAlPZVqqk24MBJlaNwrrhd17bC9d4bG8bE8a4E2A/H/V0yZE+Cz+cPmoqvJtp/YCw/QEdn",
            "__VIEWSTATEGENERATOR": "C2EE9ABB",
            "__ASYNCPOST": "true",
            "btnLogin": "Log in"
        }, headers={
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "http://localhost/targetprocess/login.aspx",
            "Cache-Control": "no-cache",
            "X-MicrosoftAjax": "Delta=true",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://localhost/targetprocess/login.aspx",
        })

    def subscribe_to_slice_notifications(self):
        connection = signalr.Connection('{0}/notifications'.format(self.parent.host), self.client)

        def notify_changed(data):
            request_success.fire(
                request_type='WS',
                name='/notifications/connect',
                response_time=0,
                response_length=0,
            )

        #make sure to get hubs before starting connection!
        slice_hub = connection.hub('Slice')
        connection.start()
        slice_hub.client.notifyChanged = lambda data: notify_changed(data)
        slice_hub.server.Subscribe({
            "parameters": self.definition,
            "clientId": "slice/1438693676288/12c64e13-f776-4739-80fa-4f77d6f44e9e235",
            "id": "bf3a2067-4ade-e84e-3a1c-dff12f8a66e8",
            "logNotifications": None
        })

    def get_acid(self):
        response = self.client.get("/restui/board.aspx",
                                   headers={
                                       "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
                                   })
        parsed = urlparse.urlparse(response.url)
        return urlparse.parse_qs(parsed.query).get('acid')[0]

    def get_slice_definition(self):
        acid = '5A68575EE7C5304C39A090CDFE425EBE'  # self.get_acid()
        return {
            "base64": "true",
            "take": 125,
            "definition": {
                "global": {
                    "acid": acid
                },
                "x": {
                    "id": None,
                    "ordering": None
                },
                "user": {
                    "cardsFilter": ""
                },
                "y": {
                    "id": None,
                    "ordering": None
                },
                "cells": {
                    "items": [
                        {
                            "id": "userstory",
                            "data": "{cardData:{id,name, type:entityType.name, projectId:project.id,entityState.isFinal, teamId:team.id, priority.importance},entity_name_small_sizes:{name},effort_total:{effort,units}}",
                            "filter": None,
                            "ordering": None
                        }
                    ],
                    "ordering": {
                        "name": "Rank",
                        "direction": "Desc"
                    }
                }
            }
        }

    @task(1)
    def get_cells(self):
        self.client.post("/slice/v1/matrix/cells",
                         json=self.definition,
                         headers={
                             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
                         })

    @task(1)
    def create_user_story(self):
        self.client.post("/slice/v1/matrix/addData",
                         json={
                             "base64": True,
                             "type": "UserStory",
                             "values": [
                                 {
                                     "id": "Name",
                                     "value": "us1",
                                     "type": "Text"
                                 },
                                 {
                                     "id": "Project",
                                     "value": "2",
                                     "type": "DDL"
                                 }
                             ],
                             "definition": self.definition.get("definition")
                         },
                         headers={
                             "Content-Type": "application/json; charset=UTF-8",
                             "Accept": "application/json, text/javascript, */*; q=0.01",
                             "X-Requested-With": "XMLHttpRequest",
                             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
                         })


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 5000


statsd = StatsClient(host='192.168.1.43', port=8125, prefix="locust")


def on_request_success(request_type, name, response_time, response_length):
    """
    Event handler that get triggered on every successful request
    """
    request_name = "{0}/{1}".format(request_type, name)
    statsd.incr("requests/{0}".format(request_name))
    statsd.incr("requests/status/success/{0}".format(request_name))
    statsd.timer("requests/response/time/{0}".format(request_name), response_time)
    statsd.timer("requests/response/length/{0}".format(request_name), response_length)


def on_request_failure(request_type, name, response_time, response_length):
    """
    Event handler that get triggered on every successful request
    """
    request_name = "{0}/{1}".format(request_type, name)
    statsd.incr("requests/{0}".format(request_name))
    statsd.incr("requests/status/failure/{0}".format(request_name))
    statsd.timer("requests/response/time/{0}".format(request_name), response_time)
    statsd.timer("requests/response/length/{0}".format(request_name), response_length)


events.request_success += on_request_success
events.request_failure += on_request_failure
