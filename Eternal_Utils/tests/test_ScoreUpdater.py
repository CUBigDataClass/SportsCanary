import unittest
from Eternal_Utils.ScoreUpdater import ScoreUpdater


class TestScoreUpdater(unittest.TestCase):
    def test___init__(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.CLIENT_ID)

    def test_get_aws_mongo_db(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.get_aws_mongo_db())

    def test_get_slugs_of_games_that_need_updating(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.get_slugs_of_games_that_need_updating())

    def test_get_url_for_sport(self):
        score_updater = ScoreUpdater()
        self.assertEqual('https://www.stattleship.com/basketball/nba/', score_updater.get_url_for_sport('nba'))
        self.assertEqual('https://www.stattleship.com/hockey/nhl/', score_updater.get_url_for_sport('nhl'))
        self.assertEqual('https://www.stattleship.com/baseball/mlb/', score_updater.get_url_for_sport('mlb'))

if __name__ == '__main__':
    unittest.main()
