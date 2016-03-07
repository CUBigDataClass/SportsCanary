import unittest
import os
from Twitter_Utils import FeatureExtraction


class TestFeatureExtractor(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_create_feature_vector(self):
        feature_extractor = FeatureExtraction.FeatureExtractor()
        tweet = 'I test this'
        expected = ['I', 'test', 'this']
        self.assertEqual(expected, feature_extractor.create_feature_vector(tweet))

    def test_extract_features(self):
        feature_extractor = FeatureExtraction.FeatureExtractor()
        feature_extractor.feature_list = ['test', 'tweet', 'this']
        self.assertEqual({'contains(test)': True, 'contains(this)': True, 'contains(tweet)': True},
                         feature_extractor.extract_features('test tweet this'))

    def test_get_base_path_to_save_classifier(self):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos+15]
        else:
            path = wd
        expected = path + '/Twitter_Utils/data/classifier.pickle'
        feature_extractor = FeatureExtraction.FeatureExtractor()
        self.assertEqual(expected, feature_extractor.get_base_path_to_save_classifier())

    def test_get_base_training_file_path(self):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos+15]
        else:
            path = wd
        expected = path + '/Twitter_Utils/data/training_set_short.csv'
        feature_extractor = FeatureExtraction.FeatureExtractor()
        self.assertEqual(expected, feature_extractor.get_base_training_file_path())

    def test_get_sentiment(self):
        feature_extractor = FeatureExtraction.FeatureExtractor()
        self.assertEqual('negative', feature_extractor.get_sentiment('0'))
        self.assertEqual('neutral', feature_extractor.get_sentiment('2'))
        self.assertEqual('positive', feature_extractor.get_sentiment('4'))
        self.assertEqual('nil', feature_extractor.get_sentiment('-1'))

    def test_remove_duplicates(self):
        feature_extractor = FeatureExtraction.FeatureExtractor()
        expected = [1, 2, 3]
        feature_extractor.feature_list = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        feature_extractor.remove_duplicates()
        self.assertEqual(expected, feature_extractor.feature_list)

    def test_create_tweets_list_with_sentiment(self):
        feature_extractor = FeatureExtraction.FeatureExtractor()
        self.assertIsNotNone(feature_extractor.create_tweets_list_with_sentiment())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
