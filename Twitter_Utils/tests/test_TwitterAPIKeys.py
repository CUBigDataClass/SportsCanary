import unittest
import os
from Twitter_Utils import TwitterAPIKeys


class TestTwitterAPIKeyHandler(unittest.TestCase):
    def setUp(self):
        twitter_api_key = TwitterAPIKeys.TwitterAPIKeyHandler()
        path = twitter_api_key.key_check_write_path
        fo = open(path, 'w')
        fo.write('[{"key_name": "Key_0", "in_use": false}, {"key_name": "Key_1", "in_use": false}]')
        fo.close()
        # register remove function
        self.addCleanup(os.remove, path)

    def test___init__(self):
        # twitter_api_key_handler = TwitterAPIKeyHandler()
        assert True

    def test_get_api_keys_from_environment_number_of_keys(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        array_of_keys = twitter_api_key_handler.get_api_keys_from_environment()
        # Test size of array
        self.assertEqual(len(array_of_keys), twitter_api_key_handler.number_of_keys)

    def test_gets_a_valid_environment_key(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        array_of_keys = twitter_api_key_handler.get_api_keys_from_environment()
        # Test content of array
        self.assertEqual(array_of_keys[0]['app_secret'], os.environ['TWITTER_APP_SECRET_0'])

    def test_check_which_key_to_use(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        expected = twitter_api_key_handler.check_which_key_to_use()
        self.assertEqual(expected, 0)

    def test_clear_api_key_at_index_for_use(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        twitter_api_key_handler.check_which_key_to_use()
        expected = twitter_api_key_handler.clear_api_key_at_index_for_use(0)
        self.assertEqual(expected, True)

    def test_get_api_keys_from_environment(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        expected = twitter_api_key_handler.get_api_keys_from_environment()
        self.assertIsNotNone(expected)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
