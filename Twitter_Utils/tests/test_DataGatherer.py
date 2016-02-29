import unittest
import os
from Twitter_Utils.DataGatherer import DataGatherer


class TestDataGatherer(unittest.TestCase):
    def test___init__(self):
        # data_gatherer = DataGatherer()
        assert True  # TODO: implement your test here

    def test_get_base_directory_path(self):
        data_gatherer = DataGatherer()
        data_gatherer.game_name_to_store = ''

        path = os.getcwd() + '/Twitter_Utils/data/tweets/'
        self.assertEqual(path, data_gatherer.get_base_directory_path())

    def test_get_base_file_path(self):
        data_gatherer = DataGatherer()
        data_gatherer.game_name_to_store = '1'
        path = os.getcwd() + '/Twitter_Utils/data/tweets/1/1.txt'
        self.assertEqual(path, data_gatherer.get_base_file_path())

    def test_on_error(self):
        data_gatherer = DataGatherer()
        self.assertEqual(False, data_gatherer.on_error('420'))

    def test_on_status(self):
        # data_gatherer = DataGatherer()
        # self.assertEqual(expected, data_gatherer.on_status(status))
        assert True  # TODO: implement your test here


if __name__ == '__main__': # pragma: no cover
    unittest.main()
