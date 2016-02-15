# coding=utf-8
from nltk.corpus import twitter_samples
import re

input_file = twitter_samples.abspath("tweets.20150430-223406.json")

"""
NLTK Guide
After importing text

text1.similar("WORD") returns words with similar meaning to what we are searching for.

After doing some NLP research it seems that there is a thing called a stop word list,
that essentially means a list of words that add nothing of value to NLP, so we strip these
from the tweets.

http://www.ranks.nl/stopwords for source

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
        original_tweet = tweet
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

        # Remove's everything that isn't a letter or space
        tweet = re.sub(r'[^a-zA-Z ]','', tweet)

        # Remove repeated char's, currently replaces it with two, could replace it with one and have it check a dictionary?
        tweet = re.sub(r'(.)\1+', r'\1\1', tweet)

        stop_word_list = ['a','about','above','after','again','against',
                  'all','am','an','and','any','are','aren\'t','as',
                  'at','be','because','been','before','being',
                  'below','between','both','but','by','can\'t',
                  'cannot','could','couldn\'t','did','didn\'t',
                  'do','does','doesn\'t','doing','don\'t','down',
                  'during','each','few','for','from','further',
                  'had','hadn\'t','has','hasn\'t','have','haven\'t',
                  'having','he','he\'d','he\'ll','he\'s','her','here',
                  'here\'s','hers','herself','him','himself','his',
                  'how','how\'s','i','i\'d','i\'ll','i\'m','i\'ve',
                  'if','in','into','is','isn\'t','it','it\'s','its',
                  'itself','let\'s','me','more','most','mustn\'t',
                  'my','myself','no','nor','not','of','off','on',
                  'once','only','or','other','ought','our','ours',
                  'ourselves','out','over','own','same','shan\'t',
                  'she','she\'d','she\'ll','she\'s','should',
                  'shouldn\'t','so','some','such','than','that',
                  'that\'s','the','their','theirs','them','themselves',
                  'then','there','there\'s','these','they','they\'d',
                  'they\'ll','they\'re','they\'ve','this','those',
                  'through','to','too','under','until','up','very',
                  'was','wasn\'t','we','we\'d','we\'ll','we\'re',
                  'we\'ve','were','weren\'t','what','what\'s','when',
                  'when\'s','where','where\'s','which','while','who',
                  'who\'s','whom','why','why\'s','with','won\'t','would',
                  'wouldn\'t','you','you\'d','you\'ll','you\'re','you\'ve',
                  'your','yours','yourself','yourselves', 'USER', 'URL']

        for word in tweet.split(" "):
            if word in stop_word_list:
                tweet = re.sub(word, '', tweet)

        # Remove extra whitespaces
        tweet = re.sub(r'[\s]+', ' ', tweet)

        return tweet
