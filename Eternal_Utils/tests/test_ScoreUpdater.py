import unittest
from Eternal_Utils.ScoreUpdater import ScoreUpdater


class TestScoreUpdater(unittest.TestCase):
    def test___init__(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.CLIENT_ID)

    def test_get_aws_mongo_db(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.get_aws_mongo_db_admin())

    def test_get_slugs_of_games_that_need_updating(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.get_slugs_of_games_that_need_updating())

    def test_get_url_for_sport(self):
        score_updater = ScoreUpdater()
        self.assertEqual('https://www.stattleship.com/basketball/nba/', score_updater.get_url_for_sport('nba'))
        self.assertEqual('https://www.stattleship.com/hockey/nhl/', score_updater.get_url_for_sport('nhl'))
        self.assertEqual('https://www.stattleship.com/baseball/mlb/', score_updater.get_url_for_sport('mlb'))

    def test_count_number_of_right_and_wrong_predictions(self):
        score_updater = ScoreUpdater()
        self.assertGreater(score_updater.count_number_of_right_and_wrong_predictions(), 40)

    def test_get_all_documents(self):
        score_updater = ScoreUpdater()
        self.assertGreaterEqual(len(score_updater.get_all_documents()), 61)

    def test_get_documents_that_are_missing_team_names(self):
        score_updater = ScoreUpdater()
        self.assertEqual([], score_updater.get_documents_that_are_missing_team_names())

    def test_get_results_for_date(self):
        score_updater = ScoreUpdater()
        self.assertEqual(21, len(score_updater.get_results_for_date('2016-04-13')))

    def test_get_success_percentage(self):
        score_updater = ScoreUpdater()
        self.assertEqual(50, score_updater.get_success_percentage(50, 50))

    def test_get_teams_in_game_tuple(self):
        score_updater = ScoreUpdater()
        expected = 'Team_1', 'Team_2'
        self.assertEqual(expected, score_updater.get_teams_in_game_tuple('Team_1 vs Team_2'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
