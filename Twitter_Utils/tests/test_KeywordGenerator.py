import unittest
from Twitter_Utils.KeywordGenerator import KeywordGenerator


class TestKeywordGenerator(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_generate_search_terms(self):
        keyword_generator = KeywordGenerator()
        # Fake ID
        self.assertEqual([], keyword_generator.generate_search_terms('FAKE TEAM ID', "nba"))
        # Actual ID
        expected_list = ['TrueToAtlanta', 'TrueToAtlanta', 'ATL', 'Hawks', 'DennisSchroder', 'ThaboSefolosha', 'TimHardawayJr.', 'PaulMillsap', 'MikeScott', 'JeffTeague', 'MikeMuscala', 'KyleKorver', 'AlHorford', 'KentBazemore', 'goTrueToAtlanta', 'goTrueToAtlanta', 'goATL', 'goHawks', 'goDennisSchroder', 'goThaboSefolosha', 'goTimHardawayJr.', 'goPaulMillsap', 'goMikeScott', 'goJeffTeague', 'goMikeMuscala', 'goKyleKorver', 'goAlHorford', 'goKentBazemore', 'Dennis Schroder', 'Thabo Sefolosha', 'Tim Hardaway Jr.', 'Paul Millsap', 'Mike Scott', 'Jeff Teague', 'Mike Muscala', 'Kyle Korver', 'Al Horford', 'Kent Bazemore']
        self.assertEqual(expected_list, keyword_generator.generate_search_terms('20901970-53a0-417c-b5b4-832a74148af6',
                                                                                "nba"))

    def test_generate_search_terms_should_throw_exception(self):
        keyword_generator = KeywordGenerator()
        keyword_generator.team_data_path = ''
        with self.assertRaises(IOError) as context:
            keyword_generator.generate_search_terms('20901970-53a0-417c-b5b4-832a74148af6', "notARealSport")
        assert True

    def test_append_word_with_go_to_list(self):
        keyword_generator = KeywordGenerator()
        test_list = ['test', 'ok']
        self.assertEqual(['test', 'ok', 'gotest', 'gook'], keyword_generator.append_word_with_go_to_list(test_list))
        # No words
        test_list = []
        self.assertEqual([], keyword_generator.append_word_with_go_to_list(test_list))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
