import os
import unittest
from Twitter_Utils.KeywordGenerator import KeywordGenerator


class TestKeywordGenerator(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_generate_search_terms_should_throw_exception(self):
        keyword_generator = KeywordGenerator()
        keyword_generator.team_data_path = ''
        with self.assertRaises(IOError):
            keyword_generator.generate_search_terms('20901970-53a0-417c-b5b4-832a74148af6', "notARealSport")
        assert True

    def test_append_word_with_go_to_list(self):
        keyword_generator = KeywordGenerator()
        test_list = ['test', 'ok']
        self.assertEqual(['test', 'ok', 'gotest', 'gook'], keyword_generator.append_word_with_go_to_list(test_list))
        # No words
        test_list = []
        self.assertEqual([], keyword_generator.append_word_with_go_to_list(test_list))

    def test_get_team_data_path_for_nhl(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/nhl-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("nhl"))

    def test_get_team_data_path_for_nba(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/nba-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("nba"))

    def test_generate_search_terms(self):
        keyword_generator = KeywordGenerator()
        team_id = '84eb19ca-1e66-416f-9e00-90b20fe4bb5e'
        sport = 'nba'
        self.assertGreater(len(keyword_generator.generate_search_terms(team_id, sport)), 5)
        team_id = 'b6bc24e7-bd37-461e-a7b2-af79f68b2438'
        sport = 'nhl'
        self.assertGreater(len(keyword_generator.generate_search_terms(team_id, sport)), 5)
        team_id = '94acb560-6d9c-4b89-a32c-7fb817ad7aa7'
        sport = 'mlb'
        self.assertGreater(len(keyword_generator.generate_search_terms(team_id, sport)), 5)

    def test_get_team_data_path_nba(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/nba-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("nba"))

    def test_get_team_data_path_mlb(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/mlb-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("mlb"))

    def test_get_team_data_path_nhl(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/nhl-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("nhl"))

    def test_get_team_data_path(self):
        keyword_generator = KeywordGenerator()
        expected_nba = os.getcwd() + '/Twitter_Utils/data/nba-teams-data.json'
        expected_nhl = os.getcwd() + '/Twitter_Utils/data/nhl-teams-data.json'
        self.assertEqual(expected_nba, keyword_generator.get_team_data_path("nba"))
        self.assertEqual(expected_nhl, keyword_generator.get_team_data_path("nhl"))

    def test_get_hashtags_for_team(self):
        keyword_generator = KeywordGenerator()
        team_id = 'eeb2db44-7894-483e-a9a7-373fb80d8e91'
        sport = 'mlb'
        expected = ['Mariners', 'Mariners']
        self.assertEqual(expected, keyword_generator.get_hashtags_for_team(team_id, sport))

        # Test exception
        team_id = 'fake-team-id-123'
        sport = 'test'
        self.assertEqual(False, keyword_generator.get_hashtags_for_team(team_id, sport))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
