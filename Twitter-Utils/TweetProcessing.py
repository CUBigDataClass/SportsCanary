# coding=utf-8
from nltk.corpus import twitter_samples
import re

input_file = twitter_samples.abspath("tweets.20150430-223406.json")

"""
NLTK Guide
After importing text

text1.similar("WORD") returns words with similar meaning to what we are searching for.


"""


class TweetProcessor:
    def __init__(self):
        pass

    @staticmethod
    def standardize_tweet(tweet):
        """
        This method seeks to standardize tweets, currently it removes RT
        from the beginning of the tweet, it replaces #'s with those words,
        it replaces @USERNAME with the code USER and it removes any extra
        whitespaces it finds.

        :param tweet: A single tweet, currently as a string, in the future
        we could change this so it takes in a tweet object, with user id and
        other params that we wish to analyze

        :return: returns a single standardized tweet object
        """
        # Convert to lowercase
        tweet = tweet.lower()

        # remove RT if it's there
        # TODO: - Some sort of counter for this would be great
        if tweet[:2] == "rt":
            tweet = tweet[3:]

        # Replace #{word} with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

        # Replace @{user} with USER
        tweet = re.sub(r'@[^\s]+', 'USER', tweet)

        # Remove extra whitespaces
        tweet = re.sub(r'[\s]+', ' ', tweet)

        # Remove URL's
        tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)

        # Remove Emoji's
        try:
        # UCS-4
            emoji_pattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        except re.error:
        # UCS-2
            emoji_pattern = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        tweet = emoji_pattern.sub('', tweet)


        # TODO: - Remove Emoticons, really anything that isn't word.
        
        return tweet
