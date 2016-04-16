import unittest
from random import randint
from Twitter_Utils.TwitterClient import TwitterClient


class TestTwitterClient(unittest.TestCase):
    def test___init__(self):
        twitter_client = TwitterClient()
        self.assertIsNot("", twitter_client.APP_KEY)
        self.assertIsNot("", twitter_client.APP_SECRET)
        self.assertIsNot("", twitter_client.OAUTH_TOKEN)
        self.assertIsNot("", twitter_client.OAUTH_TOKEN_SECRET)
        self.assertIsNotNone(twitter_client.auth)
        self.assertIsNotNone(twitter_client.api)

    def test_tweet_and_delete(self):
        twitter_client = TwitterClient()
        number = randint(0, 100)
        twitter_client.tweet('Tweeting for our test coverage! #' + str(number))
        twitter_client.delete_latest_tweet()
        assert True

    def test_create_space_separated_hashtags(self):
        twitter_client = TwitterClient()
        list_of_hashtags = ['a', 'b', 'c']
        expected = '#a #b #c'
        self.assertEqual(expected, twitter_client.create_space_separated_hashtags(list_of_hashtags))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
