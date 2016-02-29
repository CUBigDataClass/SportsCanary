import unittest
from Twitter_Utils.KeywordGenerator import KeywordGenerator


class TestKeywordGenerator(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_generate_search_terms(self):
        keyword_generator = KeywordGenerator()
        # Fake ID
        self.assertEqual([], keyword_generator.generate_search_terms('FAKE TEAM ID'))
        # Actual ID
        expected_list = ['TrueToAtlanta', 'TrueToAtlanta', 'ATL', 'Hawks', 'Atlanta',
                         'goTrueToAtlanta', 'goTrueToAtlanta', 'goATL', 'goHawks', 'goAtlanta']
        self.assertEqual(expected_list, keyword_generator.generate_search_terms('20901970-53a0-417c-b5b4-832a74148af6'))

    def test_generate_search_terms_should_throw_exception(self):
        keyword_generator = KeywordGenerator()
        keyword_generator.team_data_path = ''
        with self.assertRaises(IOError) as context:
            keyword_generator.generate_search_terms('20901970-53a0-417c-b5b4-832a74148af6')

        # self.assertTrue('This is broken' in context.exception)
        # TODO - Figure out how to make sure assertion is raised
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
