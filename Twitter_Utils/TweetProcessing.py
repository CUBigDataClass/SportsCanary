# coding=utf-8
import re
import nltk


STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
             'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
             'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
             'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
             'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
             'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
             'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
             'by', 'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below', 'to',
             'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
             'again', 'further', 'then', 'once', 'here', 'there', 'when',
             'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
             'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
             'same', 'so', 'than', 'too','very', 's', 't', 'can', 'will',
             'just', 'don', 'should', 'now', 'USER', 'URL']

class TweetProcessor:
    def __init__(self):
        self.list_of_key_words = ['nba','basketball', 'ball', 'hoops']

    def standardize_tweet(self, tweet):
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
        original_tweet = tweet
        # Convert to lowercase
        tweet = tweet.lower()

        # remove rt
        if tweet[:2] == "rt":
            tweet = tweet[3:]

        # replace # with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

        # replace @ with word
        tweet = re.sub(r'@[^\s]+', 'USER', tweet)

        # remove url
        tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)

        # remove emoji
        try:
            # UCS-4
            emoji_pattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        except re.error:
            # UCS-2
            emoji_pattern = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        tweet = emoji_pattern.sub('', tweet)

        # remove non-letter and space
        tweet = re.sub('[^a-zA-Z ]+', '', tweet)

        # remove remove repeated chars
        tweet = re.sub(r'(.)\1+', r'\1\1', tweet)

        # remove extra whitespaces
        tweet = re.sub(r'[\s]+', ' ', tweet.strip())

        # remove stop words
        words = nltk.word_tokenize(tweet)
        tweet = " ".join([x for x in words if x not in STOPWORDS])

        # remove appeneded url or user
        tweet = tweet.replace('URL','')
        tweet = tweet.replace('USER','')

        return tweet

    def check_words_in_tweet(self, tweet):
        if any(word in tweet for word in self.list_of_key_words):
            return True
        else:
            return False
