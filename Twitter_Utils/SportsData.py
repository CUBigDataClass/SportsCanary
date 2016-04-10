import logging
import datetime
import requests
import simplejson as json
from Eternal_Utils.CommonUtils import CommonUtils


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
        self.CLIENT_ID = CommonUtils.get_environ_variable('STAT_CLIENT_ID')
        self.STAT_CLIENT_SECRET = CommonUtils.get_environ_variable('STAT_CLIENT_SECRET')
        self.STAT_ACCESS_TOKEN = CommonUtils.get_environ_variable('STAT_ACCESS_TOKEN')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def get_url_for_sport(sport):
        if sport == "nba":
            return 'https://www.stattleship.com/basketball/nba/'
        elif sport == "nhl":
            return 'https://www.stattleship.com/hockey/nhl/'
        elif sport == "mlb":
            return 'https://www.stattleship.com/baseball/mlb/'

    def get_games_for_today_for_sport(self, sport):
        """
        Gets all games for today
        :param sport:
        """
        url = self.get_url_for_sport(sport) + 'games?on=today'
        self.logger.info('Getting games for today.')
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
            list_of_games.append(json.dumps({"_id": game_uuid, "start_time": game_start_time,
                                             "title": game_title, "home_team_id": game_home_team_id,
                                             "away_team_id": game_away_team_id, "slug": game_slug,
                                             "being_streamed": False,
                                             "date": datetime.datetime.now().strftime('%Y-%m-%d')}))

        list_of_games = str(list_of_games).replace("'", "")
        return list_of_games

    def get_players_for_today_for_sport(self, slug_name, team_id, sport):
        """
        Given a slug returns all team members for a given NHL team
        :param sport: nhl, nba, mlb
        :param team_id: UUID of team given by stattleship
        :param slug_name: slug name for team given by stattleship
        """
        url = self.get_url_for_sport(sport) + '/game_logs?team_id='+slug_name
        headers = {
            'Authorization': str(self.STAT_ACCESS_TOKEN),
            'Accept': 'application/vnd.stattleship.com; version=1',
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get(url, headers=headers)
            content = json.loads(res.content)
            if len(content['game_logs']) == 0:  # pragma: no cover
                return False
            if content['players']:
                return self.create_players_log_object(content['players'], team_id)
            else:  # pragma: no cover
                return False
        except KeyError:
            self.logger.error('Key error creating players log object.')
            return False

    @staticmethod
    def create_players_log_object(data, team_id):
        """
        Creates a json object from API call to Stattleship
        :param team_id:
        :param data: input of data object from Stattleship
        :return: returns JSON object with all players name & team_id for each game
        """
        list_of_players = []
        for player in data:
            if player['team_id'] == team_id:
                list_of_players.append(player['name'])
        return list_of_players
