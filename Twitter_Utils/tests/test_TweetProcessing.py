# coding=utf-8
import unittest
from Twitter_Utils.TweetProcessing import TweetProcessor


class TestTweetProcessor(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_standardize_tweet(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('justt wanted tell people',
                         tweet_processor.standardize_tweet('RT So I justttt Wanted to @FReD'
                                                           ' www.google.com tellll people that www.google.com'))

    #def test_remove_emoji(self):
        # tweet_processor = TweetProcessor()
        # self.assertEqual('', tweet_processor.remove_emoji(''))
        #assert True # TODO - Figure out how to test this
        #removed because standardize_tweet removes emojis

    def test_check_words_in_tweet(self):
        tweet_processor = TweetProcessor()
        self.assertEqual(True, tweet_processor.check_words_in_tweet('i love the nba'))

    def test_check_words_in_tweet_can_return_false(self):
        tweet_processor = TweetProcessor()
        self.assertEqual(False, tweet_processor.check_words_in_tweet('no words should match our filter'))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
