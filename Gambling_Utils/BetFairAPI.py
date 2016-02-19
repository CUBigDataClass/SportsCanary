import os
import urllib2
import json

import datetime

from Proxy import ProxyHandler


class OddsGeneration:
    def __init__(self):
        self.api_base_url = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        self.APP_KEY_DELAYED = os.environ['BET_FAIR_APP_KEY_DELAYED']
        self.APP_KEY = os.environ['BET_FAIR_APP_KEY_NONDELAYED']
        self.BET_FAIR_SESSION_TOKEN = ''
        self.BET_FAIR_USERNAME = os.environ['BET_FAIR_USERNAME']
        self.BET_FAIR_PASSWORD = os.environ['BET_FAIR_PASSWORD']
        self.api_call_headers = {}

    # TODO - We have to use a proxy to get this to work
    def get_session_key_and_set_headers(self):
        """
        Gets session key from betfair, these last 20 minutes and have to get regenerated.
        Additionally we have to create some sort of proxy for them since they hate Freedom.
        :return: session key
        """
        session_key_headers = {
            'Accept': 'application/json',
            'X-Application': self.APP_KEY_DELAYED
        }
        data = 'username=' + self.BET_FAIR_USERNAME + '&password=' + self.BET_FAIR_PASSWORD
        session_key_url = "https://identitysso.betfair.com/api/login"

        try:
            session_key_request = urllib2.Request(session_key_url, data, session_key_headers)
            proxy = ProxyHandler()
            opener = proxy.url_request()
            session_key_response = opener.open(session_key_request)
            response = session_key_response.read()
            json_response = json.loads(response)
            if json_response['status'] == 'SUCCESS':
                print json_response['token']
                self.BET_FAIR_SESSION_TOKEN = json_response['token']
                self.api_call_headers = {'X-Application': self.APP_KEY_DELAYED,
                                         'X-Authentication': self.BET_FAIR_SESSION_TOKEN,
                                         'content-type': 'application/json'}
            else:
                return False

        except urllib2.HTTPError:
            print 'Oops no service available at ' + str(session_key_url)
        except urllib2.URLError:
            print 'No service found at ' + str(session_key_url)

    def call_api(self, json_request):
        """
        This is our API caller, other functions pass in requests and it gets the info.
        :param json_request: request for information we want, based on method
        :return: returns json response from API
        """
        try:
            self.get_session_key_and_set_headers()
            request = urllib2.Request(self.api_base_url, json_request, self.api_call_headers)
            response = urllib2.urlopen(request)
            json_response = response.read()
            return json_response

        except urllib2.HTTPError:
            print 'Invalid Operation from the service: ' + str(self.api_base_url)
        except urllib2.URLError:
            print 'No service found at ' + str(self.api_base_url)

    def get_event_types(self):
        """
        Gets information for event types that bet-fair handles
        :return: returns json of events
        """
        event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
        print 'Calling listEventTypes to get event Type ID'
        response = self.call_api(event_type_req)
        event_types_json = json.loads(response)
    
        try:
            event_types = event_types_json['result']
            return event_types
        except:
            print 'Error while trying to get event types: ' + str(event_types_json['error'])

    def get_event_type_id_given_name(self, requested_event_type_name):
        """
        Input name get back event id
        :param requested_event_type_name:
        :return: id of event
        """
        event_types = self.get_event_types()
        if event_types is not None:
            for event in event_types:
                event_type_name = event['eventType']['name']
                if event_type_name == requested_event_type_name:
                    return event['eventType']['id']
        else:
            print 'Error trying to get event type id with name input.'