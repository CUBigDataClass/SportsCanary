import unittest
from Eternal_Utils.ScoreUpdater import ScoreUpdater


class TestScoreUpdater(unittest.TestCase):
    def test___init__(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.CLIENT_ID)

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
        self.assertGreater(score_updater.count_number_of_right_and_wrong_predictions('nba'), 40)

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

        # Test exception
        self.assertIsNone(score_updater.get_teams_in_game_tuple('Team_1 vs'))

    def test_get_aws_mongo_db_admin(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.get_aws_mongo_db_admin())

    def test_get_aws_mongo_db_events(self):
        score_updater = ScoreUpdater()
        self.assertIsNotNone(score_updater.get_aws_mongo_db_events())

    def test_get_team_ids_for_game(self):
        nba_slug = 'nba-2015-2016-mil-orl-2016-04-11-1900'
        mlb_slug = 'mlb-2016-mil-pit-2016-04-17-1335'
        nhl_slug = 'nhl-2015-2016-chi-stl-2016-04-15-1900'
        score_updater = ScoreUpdater()

        expected_nba = 'c7f2a75a-d6fc-4d6d-b75f-acbfb9a4aeed', '1bc89428-fb96-49cb-aae0-f6bf07a482a1'
        expected_mlb = '0644a90f-96ca-4d20-b83a-a6008462f89c', 'd6c517b0-78de-4834-8d36-b6e63b3224ee'
        expected_nhl = '4ca89483-65ae-484d-bda9-eacba9ff4915', 'a345b10e-87b5-4635-bf24-fd6be058346f'

        self.assertEqual(expected_nba, score_updater.get_team_ids_for_game(nba_slug, 'nba'))
        self.assertEqual(expected_mlb, score_updater.get_team_ids_for_game(mlb_slug, 'mlb'))
        self.assertEqual(expected_nhl, score_updater.get_team_ids_for_game(nhl_slug, 'nhl'))

    def test_get_sport_documents(self):
        score_updater = ScoreUpdater()
        scores = score_updater.get_sport_documents('nba')
        self.assertGreater(len(scores), 5)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
