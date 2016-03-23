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
        expected = ['Nets', 'Nets', 'Nets', 'RondaeHollis-Jefferson', 'BojanBogdanovic', 'ThaddeusYoung',
                    'BrookLopez', 'WayneEllington', 'ChrisMcCullough', 'MarkelBrown', 'DonaldSloan', 'WillieReed',
                    'ShaneLarkin', 'HenrySims', 'ThomasRobinson', 'SergeyKarasev', 'goNets', 'goNets', 'goNets',
                    'goRondaeHollis-Jefferson', 'goBojanBogdanovic', 'goThaddeusYoung', 'goBrookLopez',
                    'goWayneEllington', 'goChrisMcCullough', 'goMarkelBrown', 'goDonaldSloan', 'goWillieReed',
                    'goShaneLarkin', 'goHenrySims', 'goThomasRobinson', 'goSergeyKarasev', 'Rondae Hollis-Jefferson',
                    'Bojan Bogdanovic', 'Thaddeus Young', 'Brook Lopez', 'Wayne Ellington', 'Chris McCullough',
                    'Markel Brown', 'Donald Sloan', 'Willie Reed', 'Shane Larkin', 'Henry Sims', 'Thomas Robinson',
                    'Sergey Karasev']
        self.assertEqual(expected, keyword_generator.generate_search_terms(team_id, sport))

    def test_get_team_data_path_nba(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/nba-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("nba"))

    def test_get_team_data_path_nhl(self):
        keyword_generator = KeywordGenerator()
        expected = os.getcwd() + '/Twitter_Utils/data/nhl-teams-data.json'
        self.assertEqual(expected, keyword_generator.get_team_data_path("nhl"))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
