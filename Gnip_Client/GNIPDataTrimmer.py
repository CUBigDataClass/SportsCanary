import json
import os
from Twitter_Utils.TweetProcessing import TweetProcessor


class DataTrimmer:
    def __init__(self):
        self.tweet_processor = TweetProcessor()

    @staticmethod
    def get_file_location(index):
        return os.getcwd() + '/Gnip_Client/Gnip_Search_' + str(index) + '.json'

    def load_json_blob(self, counter):
        file_path = self.get_file_location(counter)
        with open(file_path) as data_file:
            return json.load(data_file)

    def get_tweets(self, r):
        tweet_set = set([])
        try:
            for i in range(r):
                json_file = self.load_json_blob(i)
                for result in json_file['results']:
                    tweet_set.add(result['body'])
                    print(self.tweet_processor.standardize_tweet(result['body']))

            return tweet_set

        except:
            print('Key "body" not found.')
            return None
