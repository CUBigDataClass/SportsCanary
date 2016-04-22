import json
import os
from Twitter_Utils.TweetProcessing import TweetProcessor
from Gnip_Client.IBMToneAnalysis import ToneAnalyzer


class DataTrimmer:
    def __init__(self):
        self.tweet_processor = TweetProcessor()
        self.tone_analyzer = ToneAnalyzer()

    @staticmethod
    def get_file_location(index):
        return os.getcwd() + '/Gnip_Client/Gnip_Searches/Gnip_Search_' + str(index) + '.json'

    def load_json_blob(self, counter):
        file_path = self.get_file_location(counter)
        with open(file_path) as data_file:
            return json.load(data_file)

    def get_tweets(self, s, r):
        tweet_set = set([])
        try:
            for i in range(s, r):
                print('At index ' + str(i))
                json_file = self.load_json_blob(i)
                for result in json_file['results']:
                    tweet = self.tweet_processor.standardize_tweet(result['body'])
                    emotions = self.tone_analyzer.query_ibm_for_tone(tweet)
                    tweet_set.add(tweet)
                    with open('output.csv', 'a+b') as analyzed_tweets:
                        if emotions[0] and emotions[1] and emotions[2] and emotions[3] and emotions[4]:
                            analyzed_tweets.write(tweet + ', ' + emotions[0] + ', ' + emotions[1] + ', '
                                              + emotions[2] + ', ' + emotions[3] + ', ' + emotions[4] + '\n')
            return tweet_set

        except:
            print('Key "body" not found.')
            return None
