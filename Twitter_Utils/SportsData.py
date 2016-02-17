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

    def get_nba_games_for_today(self):
        """Gets all games for today"""
        # TODO - Change back to today rather than date with games
        url = self.base_url + '/nba/games?on=February-18'
        headers = {
            'Authorization': str(self.STAT_ACCESS_TOKEN),
            'Accept': 'application/vnd.stattleship.com; version=1',
            'Content-Type': 'application/json'
        }

        res = requests.get(url, headers=headers)
        content = json.loads(res.content)
        return self.create_game_log_object(content['games'])

    @staticmethod
    def create_game_log_object(data):
        """
        Creates a json object from API call to Stattleship
        :param data: input of data object from Stattleship
        :return: returns JSON object with relevant information for each game
        """
        list_of_games = []
        for game in data:
            game_uuid = game['id']
            game_start_time = game['started_at']
            game_title = game['title']
            game_home_team_id = game['home_team_id']
            game_away_team_id = game['away_team_id']
            game_slug = game['slug']
            list_of_games.append(json.dumps({"uuid": game_uuid, "start_time": game_start_time,
                                             "title": game_title, "home_team_id": game_home_team_id,
                                             "away_team_id": game_away_team_id, "slug": game_slug,
                                             "being_streamed": False}))

        list_of_games = str(list_of_games).replace("'", "")
        return list_of_games
