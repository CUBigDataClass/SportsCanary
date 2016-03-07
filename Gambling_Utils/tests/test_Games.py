import unittest
from Gambling_Utils import Games


class TestGames(unittest.TestCase):
    def test___init__(self):
        assert True

    def test___str__(self):
        # games = Games(json_game_details)
        # self.assertEqual(expected, games.__str__())
        assert True  # TODO: implement your test here

    def test_get_game_country_code(self):
        # self.assertEqual(expected, games.get_game_country_code())
        assert True  # TODO: implement your test here

    def test_get_game_name(self):
        # json_game_details = '{"event": {"name": "Test Case","openDate" : "2016-02-29T19:30:00-08:00",' \
        #                     '"timezone" : "UTC", "countryCode" : "MX" } }'
        # games = Games.Games(json_game_details)
        # self.assertEqual('Test Case', games.get_game_name())
        assert True  # TODO: implement your test here

    def test_get_game_time(self):
        # games = Games(json_game_details)
        # self.assertEqual(expected, games.get_game_time())
        assert True  # TODO: implement your test here

    def test_get_game_time_zone(self):
        # games = Games(json_game_details)
        # self.assertEqual(expected, games.get_game_time_zone())
        assert True  # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
