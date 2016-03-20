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

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
