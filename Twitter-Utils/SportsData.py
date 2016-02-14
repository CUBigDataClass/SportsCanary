import os
import requests
import simplejson as json


class SportsData:
    """
    Class to gather data from the Stattleship API

    Endpoints follow the pattern <sport>/<league>/<action>
    And the headers must look as follows:

    Content-Type: application/json"
    Accept: application/vnd.stattleship.com; version=1
    Authorization: Token token=ACCESS_TOKEN
    """

    def __init__(self):
        self.CLIENT_ID = os.environ['STAT_CLIENT_ID']
        self.STAT_CLIENT_SECRET = os.environ['STAT_CLIENT_SECRET']
        self.STAT_ACCESS_TOKEN = os.environ['STAT_ACCESS_TOKEN']
        self.base_url = 'https://www.stattleship.com/basketball/'

    def get_all_basketball_games(self):

        """
        Gets all basketball games
        :return: returns content of response
        """

        url = self.base_url + '/nba/games'
        headers = {
            'Authorization': str(self.STAT_ACCESS_TOKEN),
            'Accept': 'application/vnd.stattleship.com; version=1',
            'Content-Type': 'application/json'
        }

        res = requests.get(url, headers=headers)
        content = json.loads(res.content)

        return content['games']

    def get_games_within_time_range(self):
        games = self.get_all_basketball_games()
        print games


t = SportsData()
t.get_games_within_time_range()
