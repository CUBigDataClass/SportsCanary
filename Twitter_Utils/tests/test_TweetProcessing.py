# coding=utf-8
import unittest
from Twitter_Utils.TweetProcessing import TweetProcessor

class TestTweetProcessor(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_remove_rt(self):
        tweet_processor = TweetProcessor()
        tweet = 'rt test'
        self.assertEqual('test', tweet_processor.remove_rt(tweet))
        tweet = 'no test'
        self.assertEqual('no test', tweet_processor.remove_rt(tweet))

    def test_standardize_tweet(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('justt wanted tell people',
                         tweet_processor.standardize_tweet('RT So I justttt Wanted to @FReD'
                                                           ' www.google.com tellll people that www.google.com'))

    def test_remove_appended_url_or_user(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('test ting', tweet_processor.remove_appended_url_or_user('testURL tingUSER'))

    def test_remove_emoji(self):
        # tweet_processor = TweetProcessor()
        # self.assertEqual('', tweet_processor.remove_emoji(''))
        assert True # TODO - Figure out how to test this

    def test_remove_extra_whitespaces(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('this is what it should look like',
                         tweet_processor.remove_extra_whitespaces('this   is   what it should look   like'))

    def test_remove_non_letter_and_space(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('test ing', tweet_processor.remove_non_letter_and_space('test!@#$%^&*()12334567890 ing'))

    def test_remove_repeated_chars(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('tessttingg', tweet_processor.remove_repeated_chars('tessssssssssssssssttttttttingggg'))

    def test_remove_url(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('testing URL URL', tweet_processor.remove_url('testing www.google.com https://www.testing.com'))

    def test_replace_at_with_word(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('USER tell USER about USER go USER',
                         tweet_processor.replace_at_with_word('@fred tell @me about @twitter go @buffs'))

    def test_replace_hashtag_with_word(self):
        tweet_processor = TweetProcessor()
        self.assertEqual('testing go buffs go heat nba',
                         tweet_processor.replace_hashtag_with_word('testing #go #buffs go #heat #nba'))

if __name__ == '__main__':
    unittest.main()
