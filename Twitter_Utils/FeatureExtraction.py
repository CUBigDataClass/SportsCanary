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

    def extract_feature(self):
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
        return os.getcwd() + '/Twitter_Utils/data/training_set_short.csv'

    @staticmethod
    def get_base_path_to_save_classifier():
        return os.getcwd() + '/Twitter_Utils/data/classifier.pickle'

    def remove_duplicates(self):
        self.feature_list = list(set(self.feature_list))

    def extract_features(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.feature_list:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    def save_classifier(self, classifier):
        print 'Saving new classifier.'
        try:
            f = open(self.get_base_path_to_save_classifier(), 'wb')
            pickle.dump(classifier, f)
            f.close()
        except IOError:
            print 'Error'
            return False

    def load_classifier(self):
        try:
            f = open(self.get_base_path_to_save_classifier(), 'rb')
            classifier = pickle.load(f)
            f.close()
            return classifier
        except IOError:
            print 'No classifier was found.'
            return None

    def create_training_set(self):
        print 'Creating new classifier.'
        tweets = self.extract_feature()
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

    def analyze_tweets(self):
        naive_bayes_classifier = self.load_classifier()
        if naive_bayes_classifier is None:
            naive_bayes_classifier = self.create_training_set()

        with open(os.getcwd() + '/Twitter_Utils/data/tweets/2016-03-01-Hawks-vs-Warriors/2016-03-01-Hawks-vs-Warriors.txt') as f:
            for line in f:
                print naive_bayes_classifier.classify(self.extract_features(self.create_feature_vector(line)))

k = FeatureExtractor()
k.analyze_tweets()
