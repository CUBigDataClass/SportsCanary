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

    def test_create_training_set(self):
        # feature_extractor = FeatureExtractor()
        # self.assertEqual(expected, feature_extractor.create_training_set())
        assert True # TODO: implement your test here

    def test_extract_feature(self):
        # feature_extractor = FeatureExtractor()
        # self.assertEqual(expected, feature_extractor.extract_feature())
        assert True # TODO: implement your test here

    def test_extract_features(self):
        # feature_extractor = FeatureExtractor()
        # self.assertEqual(expected, feature_extractor.extract_features(tweet))
        assert True # TODO: implement your test here

    def test_get_base_path_to_save_classifier(self):
        expected = os.getcwd() + '/Twitter_Utils/data/NB.txt'
        feature_extractor = FeatureExtraction.FeatureExtractor()
        self.assertEqual(expected, feature_extractor.get_base_path_to_save_classifier())

    def test_get_base_training_file_path(self):
        expected = os.getcwd() + '/Twitter_Utils/data/training_set_short.csv'
        feature_extractor = FeatureExtraction.FeatureExtractor()
        self.assertEqual(expected, feature_extractor.get_base_training_file_path())

    def test_get_sentiment(self):
        # feature_extractor = FeatureExtractor()
        # self.assertEqual(expected, feature_extractor.get_sentiment())
        assert True  # TODO: implement your test here

    def test_remove_duplicates(self):
        feature_extractor = FeatureExtraction.FeatureExtractor()
        expected = [1, 2, 3]
        feature_extractor.feature_list = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        feature_extractor.remove_duplicates()
        self.assertEqual(expected, feature_extractor.feature_list)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
