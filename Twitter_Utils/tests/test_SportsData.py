import json
import unittest
import datetime
from Twitter_Utils.SportsData import SportsData


class TestSportsData(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_get_nba_games_for_today(self):
        sports_data = SportsData()
        result = sports_data.get_games_for_today_for_sport("nba")
        self.assertIsNotNone(result)

    def test_create_game_log_object(self):
        sports_data = SportsData()
        self.assertEqual('[]', sports_data.create_game_log_object([]))
        data = [{'interval_type': 'regularseason', 'wind_direction': None, 'updated_at': '2016-01-06T03:17:52-05:00',
                 'season_id': 'e56321f3-1c81-4f91-9bdf-8dac07129648', 'duration': None,
                 'started_at': '2016-02-18T19:30:00-08:00', 'id': '4b2fb0bc-864c-4ede-be61-59ed14e1da50',
                 'attendance': 0, 'temperature': None, 'title': 'Spurs vs Clippers', 'away_team_outcome': 'undecided',
                 'weather_conditions': None, 'daytime': False, 'label': 'Spurs vs Clippers', 'score': '0-0',
                 'at_neutral_site': False, 'away_team_id': 'ed803cc0-8e6e-4798-b5aa-9eecbc977801',
                 'winning_team_id': None, 'status': 'upcoming', 'score_differential': 0, 'timestamp': 1455852600,
                 'temperature_unit': None, 'venue_id': '093c73fa-ca95-4761-8047-5057a2e4ae9d',
                 'scoreline': 'Spurs 0 - Clippers 0', 'interval_number': '', 'home_team_outcome': 'undecided',
                 'slug': 'nba-2015-2016-sa-lac-2016-02-18-1930', 'wind_speed': None, 'on': 'on February 18, 2016',
                 'ended_at': None, 'name': 'Spurs vs Clippers February 18, 2016 at  7:30pm',
                 'created_at': '2016-01-06T03:17:52-05:00', 'interval': 'Regular Season',
                 'home_team_id': '5bf2300f-777b-4caa-9ef3-3fda11f17ad1', 'away_team_score': 0, 'wind_speed_unit': None,
                 'home_team_score': 0}]

        expected_response = [{"_id": "4b2fb0bc-864c-4ede-be61-59ed14e1da50", "title": "Spurs vs Clippers",
                              "date": datetime.datetime.now().strftime('%Y-%m-%d'),
                              "start_time": "2016-02-18T19:30:00-08:00", "slug": "nba-2015-2016-sa-lac-2016-02-18-1930",
                              "home_team_id": "5bf2300f-777b-4caa-9ef3-3fda11f17ad1",
                              "away_team_id": "ed803cc0-8e6e-4798-b5aa-9eecbc977801", "being_streamed": False}]
        expected_response = json.dumps(expected_response)
        self.assertEqual(expected_response, sports_data.create_game_log_object(data))

    def test_get_nba_players_for_today(self):
        sports_data = SportsData()
        result = sports_data.get_players_for_today_for_sport('nba-dal', '35ded680-b7b1-4cd9-a223-7bc4ab0b77ed', "nba")
        self.assertIsNot(False, result)

    def test_get_nhl_games_for_today(self):
        sports_data = SportsData()
        self.assertIsNotNone(sports_data.get_games_for_today_for_sport("nhl"))

    def test_get_games_for_today_for_sport_nba(self):
        sports_data = SportsData()
        self.assertIsNot(0, sports_data.get_games_for_today_for_sport("nba"))

    def test_get_games_for_today_for_sport_nhl(self):
        sports_data = SportsData()
        self.assertIsNot(0, sports_data.get_games_for_today_for_sport("nhl"))

    # def test_get_nhl_players_for_today(self):
    #     sports_data = SportsData()
    #     result = sports_data.get_players_for_today_for_sport('nhl-ana', '0e39b5fe-bbac-4488-8a4c-6556fa1fff88', "nhl")
    #     self.assertIsNot(False, result)

    def test_get_mlb_players_for_today(self):
        sports_data = SportsData()
        result = sports_data.get_players_for_today_for_sport('mlb-bos', '4c2ad3df-a7fd-458d-a412-6e31574a0b7b', "mlb")
        self.assertIsNot(False, result)

    def test_get_url_for_sport(self):
        sports_data = SportsData()
        expected_nba = 'https://www.stattleship.com/basketball/nba/'
        expected_nhl = 'https://www.stattleship.com/hockey/nhl/'
        self.assertEqual(expected_nba, sports_data.get_url_for_sport("nba"))
        self.assertEqual(expected_nhl, sports_data.get_url_for_sport("nhl"))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
