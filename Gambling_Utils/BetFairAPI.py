import urllib2
import json
from Eternal_Utils.CommonUtils import CommonUtils
from Gambling_Utils.Games import Games
from Gambling_Utils.Game import Game

from Proxy import ProxyHandler


class OddsGeneration:
    def __init__(self):
        self.api_base_url = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        self.APP_KEY_DELAYED = CommonUtils.get_environ_variable('BET_FAIR_APP_KEY_DELAYED')
        self.APP_KEY = CommonUtils.get_environ_variable('BET_FAIR_APP_KEY_NONDELAYED')
        self.BET_FAIR_SESSION_TOKEN = CommonUtils.get_environ_variable('BET_FAIR_SESSION_TOKEN')
        self.BET_FAIR_USERNAME = CommonUtils.get_environ_variable('BET_FAIR_USERNAME')
        self.BET_FAIR_PASSWORD = CommonUtils.get_environ_variable('BET_FAIR_PASSWORD')
        self.api_call_headers = {}

    def set_session_key_headers(self):
        session_key_headers = {
            'Accept': 'application/json',
            'X-Application': self.APP_KEY_DELAYED
        }
        return session_key_headers

    def set_data_for_session(self):
        return 'username=' + self.BET_FAIR_USERNAME + '&password=' + self.BET_FAIR_PASSWORD

    @staticmethod
    def set_session_key_url():
        return "https://identitysso.betfair.com/api/login"

    @staticmethod
    def create_urllib2_request(session_key_url, data, session_key_headers):
        return urllib2.Request(session_key_url, data, session_key_headers)

    def get_session_key_and_set_headers(self):
        """
        Gets session key from betfair, these last 20 minutes and have to get regenerated.
        Additionally we have to create some sort of proxy for them since they hate Freedom.
        :return: session key
        """
        session_key_headers = self.set_session_key_headers()
        data = self.set_data_for_session()
        session_key_url = self.set_session_key_url()

        try:
            session_key_request = self.create_urllib2_request(session_key_url, data, session_key_headers)
            proxy = ProxyHandler()
            opener = proxy.url_request()
            session_key_response = opener.open(session_key_request)
            response = session_key_response.read()
            json_response = json.loads(response)
            self.set_session_token_and_api_call_headers(json_response)

        except urllib2.HTTPError:  # pragma: no cover
            print 'Oops no service available at ' + str(session_key_url)
            raise urllib2.HTTPError
        except urllib2.URLError:  # pragma: no cover
            print 'No service found at ' + str(session_key_url)
            raise urllib2.URLError

    def set_session_token_and_api_call_headers(self, json_response):
        if json_response['status'] == 'SUCCESS':
            self.BET_FAIR_SESSION_TOKEN = json_response['token']
            self.api_call_headers = {'X-Application': self.APP_KEY_DELAYED,
                                     'X-Authentication': self.BET_FAIR_SESSION_TOKEN,
                                     'content-type': 'application/json'}
            return self.BET_FAIR_SESSION_TOKEN
        else:
            return False

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

        except urllib2.HTTPError:  # pragma: No cover
            print 'Invalid Operation from the service: ' + str(self.api_base_url)
        except urllib2.URLError:  # pragma: No cover
            print 'No service found at ' + str(self.api_base_url)

    def get_list_events_filtered(self, game):
        """
        This method gives out the list of games filtered by the given pattern
        :param game : game name pattern to search for :
        :return json response (list of such games) from API:
        """
        self.get_session_key_and_set_headers()
        json_request = '[{ "jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", ' \
                       '"params": { "filter": { "textQuery":"' + game + '" } },"id": 1}]'
        response = self.call_api(json_request)
        events = json.loads(response)
        return events

    def get_particular_event_list(self, game_id, game_start_from, game_end_at):
        """
        method to obtain game information based on game_id
        :param game_start_from: filter start date with time
        :param game_end_at: filter end date with time
        :param game_id: id of the game in the Betfair APT db.
        Id of the game can be found out from get_list_events_filtered method
        :return game information of that particular game:
        """
        event_type_req = '[{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listEvents","params": ' \
                         '{"filter": {"eventTypeIds": ["' + game_id + '"], "marketStartTime": {"from": ' \
                         '"' + game_start_from + '","to": "' + game_end_at + '"}}},"id": 1}]'
        response = self.call_api(event_type_req)
        event_list_json = json.loads(response)

        try:
            event_list = event_list_json[0]['result']
            return event_list
        except KeyError:
            print 'Error while trying to get event types: ' + str(event_list_json['error'])

    def get_games(self, game_name, start_time, end_time):
        """
        :param game_name: name of the name to be queried on BetFair
        :param start_time: query time range start
        :param end_time: query time range end
        :return: list of game events
        """
        response = self.get_list_events_filtered(game_name)
        try:
            game_events = []
            for r in response[0]["result"]:
                game_events += [Game(r)]

            for g in game_events:
                bb_game_list = self.get_particular_event_list(g.id, start_time, end_time)
                for i in range(len(bb_game_list)):
                    game_detail = Games(bb_game_list[i])
                    g.add_games(game_detail)

            return game_events
        except KeyError:
            print 'Error accumulating games' + str(response['error'])

