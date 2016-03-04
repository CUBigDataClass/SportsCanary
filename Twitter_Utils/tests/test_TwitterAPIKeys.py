import unittest
import os
from Twitter_Utils import TwitterAPIKeys


class TestTwitterAPIKeyHandler(unittest.TestCase):
    def test___init__(self):
        # twitter_api_key_handler = TwitterAPIKeyHandler()
        assert True

    def test_get_api_keys_from_environment_number_of_keys(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        array_of_keys = twitter_api_key_handler.get_api_keys_from_environment()
        # Test size of array
        self.assertEqual(len(array_of_keys), twitter_api_key_handler.number_of_keys)
        # Test content of array
        self.assertEqual(array_of_keys[0]['app_secret'], os.environ['TWITTER_APP_SECRET_0'])

    def test_gets_a_valid_enviorment_key(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        array_of_keys = twitter_api_key_handler.get_api_keys_from_environment()
        # Test content of array
        self.assertEqual(array_of_keys[0]['app_secret'], os.environ['TWITTER_APP_SECRET_0'])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
