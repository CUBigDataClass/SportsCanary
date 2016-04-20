import json
import unittest
import os
from datetime import datetime
from Gnip_Client.SearchClient import GnipSearchClient
from httmock import urlmatch, HTTMock


class TestGnipSearchClient(unittest.TestCase):
    def test___init__(self):
        gnip_search_client = GnipSearchClient()
        self.assertEqual(gnip_search_client.counter, 0)
        self.assertIsNotNone(gnip_search_client.username)
        self.assertIsNotNone(gnip_search_client.url)

    def test_convert_date_to_gnip_format(self):
        gnip_search_client = GnipSearchClient()
        date = datetime(2016, 04, 14, 02, 30)
        expected = '201604140230'
        self.assertEqual(expected, gnip_search_client.convert_date_to_gnip_format(date))

    def test_create_start_time(self):
        gnip_search_client = GnipSearchClient()
        expected = datetime(2016, 04, 14, 02, 30)
        self.assertEqual(expected, gnip_search_client.create_start_time())

    def test_get_file_path(self):
        gnip_search_client = GnipSearchClient()
        expected = os.getcwd() + '/Gnip_Client/Gnip_Search_1.json'
        self.assertEqual(expected, gnip_search_client.get_file_path(1))

    def test_save_json_blog_to_disk(self):
        gnip_search_client = GnipSearchClient()
        content = '{"results": [{"id": 123}]}'
        json_blob = json.loads(content)
        gnip_search_client.save_json_blog_to_disk(json_blob, 2)
        loaded_json_blob = gnip_search_client.load_json_blob(2)
        self.assertEqual(json_blob, loaded_json_blob)
        os.remove(gnip_search_client.get_file_path(2))

    @urlmatch(netloc=r'(.*\.)?gnip-api\.twitter\.com(.*)')
    def gnip_mock(self, url, request):
        return '{"results": [{"id": 123}],"next": "fake_next_token"}'

    @urlmatch(netloc=r'(.*\.)?gnip-api\.twitter\.com(.*)')
    def gnip_mock_no_next(self, url, request):
        return '{"results": [{"id": 123}]}'

    # Full integration test for search
    def test_initial_search(self):
        gnip_search_client = GnipSearchClient()

        from_date = gnip_search_client.create_start_time()
        to_date = gnip_search_client.move_date_forward_by(from_date, 01, 01, 01)

        from_date = gnip_search_client.convert_date_to_gnip_format(from_date)
        to_date = gnip_search_client.convert_date_to_gnip_format(to_date)

        # open context to patch
        with HTTMock(self.gnip_mock):
            gnip_search_client.initial_search('Fake_Query', 10, from_date, to_date, 2)

        saved_json_blob_1 = gnip_search_client.load_json_blob(0)
        saved_json_blob_2 = gnip_search_client.load_json_blob(1)
        expected_json_blob_1 = json.loads('{"results": [{"id": 123}],"next": "fake_next_token"}')
        expected_json_blob_2 = json.loads('{"results": [{"id": 123}],"next": "fake_next_token"}')
        self.assertEqual(saved_json_blob_1, expected_json_blob_1)
        self.assertEqual(saved_json_blob_2, expected_json_blob_2)

        file_to_remove_1 = os.getcwd() + '/Gnip_Client/Gnip_Search_0.json'
        file_to_remove_2 = os.getcwd() + '/Gnip_Client/Gnip_Search_1.json'
        os.remove(file_to_remove_1)
        os.remove(file_to_remove_2)

        with HTTMock(self.gnip_mock_no_next):
            gnip_search_client.initial_search('Fake_Query', 10, from_date, to_date, 1)

        saved_json_blob_1 = gnip_search_client.load_json_blob(2)
        expected_json_blob_1 = json.loads('{"results": [{"id": 123}]}')
        self.assertEqual(saved_json_blob_1, expected_json_blob_1)

        file_to_remove_3 = os.getcwd() + '/Gnip_Client/Gnip_Search_2.json'
        os.remove(file_to_remove_3)

    def test_move_date_forward_by(self):
        gnip_search_client = GnipSearchClient()
        date = datetime(2016, 04, 14, 02, 30)
        expected_date = datetime(2016, 04, 15, 03, 40)
        self.assertEqual(expected_date, gnip_search_client.move_date_forward_by(date, 1, 1, 10))

    def test_iterate_through_game_at_minute_intervals(self):
        gnip_search_client = GnipSearchClient()
        self.assertEqual(True, gnip_search_client.iterate_through_game_at_minute_intervals())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
