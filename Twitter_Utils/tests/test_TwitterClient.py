import unittest
from random import randint
from datetime import datetime
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
        # Second one to make sure we catch duplicate status
        twitter_client.tweet('Tweeting for our test coverage! #' + str(number))
        twitter_client.delete_latest_tweet()
        assert True

    def test_create_space_separated_hashtags(self):
        twitter_client = TwitterClient()
        list_of_hashtags = ['a', 'b', 'c']
        expected = '#a #b #c'
        self.assertEqual(expected, twitter_client.create_space_separated_hashtags(list_of_hashtags))

    def test_enriched_tweet_low_confidence(self):
        twitter_client = TwitterClient()
        tweet_percentage_tuple = 55, 45
        teams_tuple = 'Brewers', 'Pirates'
        slug = 'mlb-2016-mil-pit-2016-04-17-1335'
        sport = 'mlb'
        self.assertEqual(True, twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple, teams_tuple, slug, sport))
        twitter_client.delete_latest_tweet()
        tweet_percentage_tuple = 45, 55
        self.assertEqual(True, twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple, teams_tuple, slug, sport))
        twitter_client.delete_latest_tweet()

    def test_enriched_tweet_high_confidence(self):
        twitter_client = TwitterClient()
        tweet_percentage_tuple = 80, 20
        teams_tuple = 'Brewers', 'Pirates'
        slug = 'mlb-2016-mil-pit-2016-04-17-1335'
        sport = 'mlb'
        self.assertEqual(True, twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple, teams_tuple, slug, sport))
        twitter_client.delete_latest_tweet()
        tweet_percentage_tuple = 20, 80
        self.assertEqual(True, twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple, teams_tuple, slug, sport))
        twitter_client.delete_latest_tweet()

    def test_enriched_tweet_exception(self):
        twitter_client = TwitterClient()
        tweet_percentage_tuple = 55, 45
        teams_tuple = 'Brewers', 'Pirates'
        slug = 'mlb-2016-mil-pit-2016-04-17-1335'
        sport = 'mlb'
        self.assertEqual(True, twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple, teams_tuple, slug, sport))
        twitter_client.delete_latest_tweet()
        tweet_percentage_tuple = 45, 55
        self.assertEqual(True, twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple, teams_tuple, slug, sport))
        twitter_client.delete_latest_tweet()

    def test_get_day_month(self):
        twitter_client = TwitterClient()
        expected = datetime.now().strftime('%m-%d')
        self.assertEqual(expected, twitter_client.get_day_month())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
