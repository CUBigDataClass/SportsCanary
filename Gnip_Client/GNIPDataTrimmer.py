import json
import os
import pickle
from Twitter_Utils.TweetProcessing import TweetProcessor
from collections import OrderedDict
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

    # 167553 total
    def get_tweets(self, s, r):
        try:
            ordered_tweet_dict = pickle.load(open("saved_dict.p", "rb"))
            return ordered_tweet_dict
        except IOError:
            ordered_tweet_dict = OrderedDict()
            for i in range(s, r):
                try:
                    print('At index ' + str(i))
                    json_file = self.load_json_blob(i)
                    for result in json_file['results']:
                        tweet = self.tweet_processor.standardize_tweet(result['body'])

                        if tweet in ordered_tweet_dict:
                            ordered_tweet_dict[tweet] += 1
                        else:
                            ordered_tweet_dict[tweet] = 1

                except:
                    print('Key "body" not found.')
                    return None
            print("LENGTH: " + str(len(ordered_tweet_dict)))
            pickle.dump(ordered_tweet_dict, open('saved_dict.p', 'wb'))
            return ordered_tweet_dict

    def write_emotions(self, tweet_dict):
        for i, entry in enumerate(tweet_dict):
            try:
                if i > 57556:
                    print i
                    emotions = self.tone_analyzer.query_ibm_for_tone(entry)
                    with open('output.csv', 'a+b') as analyzed_tweets:
                        if emotions[0] and emotions[1] and emotions[2] and emotions[3] and emotions[4]:
                            analyzed_tweets.write(entry + ', ' + emotions[0] + ', ' + emotions[1] + ', ' + emotions[2] + ', ' +
                                                  emotions[3] + ', ' + emotions[4] + '\n')
            except:
                print('Error')

# d = DataTrimmer()
# d.write_emotions(d.get_tweets(2, 900))
