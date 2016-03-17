# coding=utf-8
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

        tweet = self.remove_rt(tweet)

        tweet = self.replace_hashtag_with_word(tweet)

        tweet = self.replace_at_with_word(tweet)

        tweet = self.remove_url(tweet)

        tweet = self.remove_emoji(tweet)

        tweet = self.remove_non_letter_and_space(tweet)

        tweet = self.remove_repeated_chars(tweet)

        tweet = self.remove_extra_whitespaces(tweet)
        
        tweet = self.remove_stop_words(tweet)

        tweet = self.remove_appended_url_or_user(tweet)

        return tweet

    @staticmethod
    def remove_rt(tweet):
        if tweet[:2] == "rt":
            return tweet[3:]
        else:
            return tweet

    @staticmethod
    def replace_hashtag_with_word(tweet):
        return re.sub(r'#([^\s]+)', r'\1', tweet)

    @staticmethod
    def replace_at_with_word(tweet):
        return re.sub(r'@[^\s]+', 'USER', tweet)

    @staticmethod
    def remove_url(tweet):
        return re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)

    @staticmethod
    def remove_emoji(tweet):
        try:
        # UCS-4
            emoji_pattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        except re.error:
        # UCS-2
            emoji_pattern = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        return emoji_pattern.sub('', tweet)

    def remove_non_letter_and_space(self, tweet):
        return re.sub('[^a-zA-Z ]+', '', tweet)

    def remove_repeated_chars(self, tweet):
        return re.sub(r'(.)\1+', r'\1\1', tweet)

    def remove_extra_whitespaces(self, tweet):
        return re.sub(r'[\s]+', ' ', tweet)

    def remove_stop_words(self, tweet):
        english_stop_words = stopwords.words('english')
        english_stop_words.extend(('USER','URL'))
        words = nltk.word_tokenize(tweet)
        return " ".join([x for x in words if x not in english_stop_words])

    def remove_appended_url_or_user(self, tweet):
        tweet = tweet.replace('URL','')
        return tweet.replace('USER','')

    def lemmatize_tweet(self, tweet):
        wordnet_lemmatizer = WordNetLemmatizer()
        new_tweet = ''
        for word in tweet:
            stemmed_word = wordnet_lemmatizer.lemmatize(word)
            new_tweet = new_tweet + stemmed_word
        print new_tweet


class Filter:
    def __init__(self):
        pass

    def check_words_in_tweet(self, tweet):
    	tweet = tweet + self.add_key_words_to_tweet()
    	long_word_set = set(tweet.split())
        if set(tweet.split()) & long_word_set:
        	print "True"

    def add_key_words_to_tweet(self):
    	word_list = ['nba','basketball', 'ball']
    	return ' '.join(word[0] for word in word_list)

f = TweetProcessor()
f.lemmatize_tweet('what does this do I am wondering if future parts of speech make a difference in this at all')