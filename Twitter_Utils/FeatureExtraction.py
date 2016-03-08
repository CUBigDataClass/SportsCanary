import csv
import nltk
import pickle
import TweetProcessing
import DataGatherer
import os
# Data Source - Sentiment140


class FeatureExtractor:
    def __init__(self):
        self.tweet_processor = TweetProcessing.TweetProcessor()
        self.data_gatherer = DataGatherer.DataGatherer()
        self.feature_list = []

    def create_tweets_list_with_sentiment(self):
        input_tweets = csv.reader(open(self.get_base_training_file_path(), 'rb'), delimiter=',')
        tweets = []
        for row in input_tweets:
            sentiment = self.get_sentiment(row[0])
            tweet = row[5]
            processed_tweet = self.tweet_processor.standardize_tweet(tweet)
            feature_vector = self.data_gatherer.create_feature_vector(processed_tweet)
            self.feature_list.extend(feature_vector)
            tweets.append((feature_vector, sentiment))
        return tweets

    @staticmethod
    def get_sentiment(sentiment):
        if sentiment == '0':
            return 'negative'
        elif sentiment == '2':
            return 'neutral'
        elif sentiment == '4':
            return 'positive'
        else:
            return 'nil'

    @staticmethod
    def get_base_training_file_path():
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: No cover
            path = wd[0:pos+15]
        else:
            path = wd
        return path + '/Twitter_Utils/data/training_set_short.csv'

    @staticmethod
    def get_base_path_to_save_classifier():
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: No cover
            path = wd[0:pos+15]
        else:
            path = wd
        return path + '/Twitter_Utils/data/classifier.pickle'

    def remove_duplicates(self):
        self.feature_list = list(set(self.feature_list))

    def extract_features(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.feature_list:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    def save_classifier(self, classifier):  # pragma: No cover
        print 'Saving new classifier.'
        try:
            f = open(self.get_base_path_to_save_classifier(), 'wb')
            pickle.dump(classifier, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except IOError:
            print 'Error while saving classifier'
            return IOError

    def load_classifier(self):  # pragma: No cover
        try:
            f = open(self.get_base_path_to_save_classifier(), 'rb')
            classifier = pickle.load(f)
            f.close()
            return classifier
        except IOError:
            print 'Error while loading classifier'
            return None

    def train_naive_bayes_classifier(self):  # pragma: No cover
        print 'Creating new classifier.'
        tweets = self.create_tweets_list_with_sentiment()
        self.remove_duplicates()
        training_set = nltk.classify.util.apply_features(self.extract_features, tweets)

        naive_bayes_classifier = nltk.NaiveBayesClassifier.train(training_set)
        self.save_classifier(naive_bayes_classifier)
        return naive_bayes_classifier

    @staticmethod
    def create_feature_vector(tweet):
        feature_vector = []
        words = tweet.split()
        for word in words:
            feature_vector.append(word)

        return feature_vector

    def analyze_tweets(self):  # pragma: No cover
        naive_bayes_classifier = self.load_classifier()
        if naive_bayes_classifier is None:
            naive_bayes_classifier = self.train_naive_bayes_classifier()
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:
            path = wd[0:pos+15]
        else:
            path = wd
        with open(path + '/Twitter_Utils/data/tweets/2016-03-01-Hawks-vs-Warriors/2016-03-01-Hawks-vs-Warriors.txt') as f:
            for line in f:
                print naive_bayes_classifier.classify(self.extract_features(self.create_feature_vector(line)))

# t = FeatureExtractor()
# t.analyze_tweets()
