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
        self.base_url = 'https://www.stattleship.com/basketball/'
        self.logger = logging.getLogger(__name__)

    def get_nba_games_for_today(self):
        """Gets all games for today"""
        self.logger.info('Getting games for today.')
        url = self.base_url + '/nba/games?on=today'
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

    def get_nba_players_for_today(self):
        """ Gets results for games played already for the day, if no games
            have been played then no results appear"""
        # TODO - Change back to today rather than date with games
        url = self.base_url + '/nba/game_logs?on=March-5'
        headers = {
            'Authorization': str(self.STAT_ACCESS_TOKEN),
            'Accept': 'application/vnd.stattleship.com; version=1',
            'Content-Type': 'application/json'
        }

        res = requests.get(url, headers=headers)
        content = json.loads(res.content)
        if len(content['game_logs']) == 0:  # pragma: no cover
            return True
        if content['players']:
            return self.create_players_log_object(content['players'])
        else:  # pragma: no cover
            return False

    @staticmethod
    def create_players_log_object(data):
        """
        Creates a json object from API call to Stattleship
        :param data: input of data object from Stattleship
        :return: returns JSON object with all players name & team_id for each game
        """
        games_id = []
        list_of_games = json.loads(SportsData().get_nba_games_for_today())
        for game in list_of_games:
            games_id.append(game.get('home_team_id'))
            games_id.append(game.get('away_team_id'))

        list_of_players = []
        for player in data:
            if player['team_id'] in games_id:
                player_name = player['name']
                player_team_id = player['team_id']
                list_of_players.append(json.dumps({"name": player_name, "team_id": player_team_id}))

        list_of_players = str(list_of_players).replace("'", "")
        return list_of_players
