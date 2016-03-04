import unittest
import os
from Twitter_Utils import TwitterAPIKeys


class TestTwitterAPIKeyHandler(unittest.TestCase):
    def setUp(self):
        twitter_api_key = TwitterAPIKeys.TwitterAPIKeyHandler()
        path = twitter_api_key.key_check_write_path
        twitter_api_key.write_initial_keys_state_to_disk()
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

    def test_check_which_key_to_use_creates_keys(self):
        twitter_api_key = TwitterAPIKeys.TwitterAPIKeyHandler()
        path = twitter_api_key.key_check_write_path
        os.remove(path)
        expected = twitter_api_key.check_which_key_to_use()
        self.assertTrue(expected)

    def test_clear_api_key_at_index_for_use(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        twitter_api_key_handler.check_which_key_to_use()
        expected = twitter_api_key_handler.clear_api_key_at_index_for_use(0)
        self.assertEqual(expected, True)

    def test_get_api_keys_from_environment(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        expected = twitter_api_key_handler.get_api_keys_from_environment()
        self.assertIsNotNone(expected)

    def test_update_json_file_can_raise_assertion(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        twitter_api_key_handler.key_check_write_path = ''
        json_file = [{'in_use': False}]
        with self.assertRaises(IOError):
            twitter_api_key_handler.update_json_file(json_file, 0)
        assert True

    def test_clear_api_key_at_index_for_use_can_raise_assertion(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        twitter_api_key_handler.key_check_write_path = ''
        json_file = [{'in_use': False}]
        with self.assertRaises(IOError):
            twitter_api_key_handler.clear_api_key_at_index_for_use(0)
        assert True

    def test_write_initial_keys_to_disk_can_raise_assertion(self):
        twitter_api_key_handler = TwitterAPIKeys.TwitterAPIKeyHandler()
        twitter_api_key_handler.key_check_write_path = 'asdf/fsdfwer'
        twitter_api_key_handler.write_initial_keys_state_to_disk()
        with self.assertRaises(IOError):
            twitter_api_key_handler.clear_api_key_at_index_for_use(0)
        assert True

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
