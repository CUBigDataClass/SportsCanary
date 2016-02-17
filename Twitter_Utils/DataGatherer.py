from TweetProcessing import TweetProcessor
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API


class DataGatherer(StreamListener):
    """ Class to gather data from Twitter
        Twitter Streaming API: https://dev.twitter.com/streaming/overview/request-parameters#track
    """

    def __init__(self):
        super(DataGatherer, self).__init__()
        self.APP_KEY = os.environ['TWITTER_APP_KEY']
        self.APP_SECRET = os.environ['TWITTER_APP_SECRET']
        self.OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
        self.OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
        self.processor = TweetProcessor()
        self.game_id_to_store = ''
        self.game_name_to_store = ''
        self.auth = OAuthHandler(self.APP_KEY, self.APP_SECRET)
        self.auth.set_access_token(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
        self.api = API(self.auth)

    def on_error(self, status_code):
        print 'ERROR: ' + status_code
        # if status_code == 420:
        # returning False in on_data disconnects the stream
        return False

    def on_status(self, status):
        if status.lang == 'en':
            processed_tweet = self.processor.standardize_tweet(status.text)
            # print processed_tweet
            self.save_tweet_to_disk(processed_tweet)

    def get_tweet_stream(self, track, game_id, game_name):
        stream = Stream(self.auth, self)
        self.game_id_to_store = game_id
        self.game_name_to_store = game_name
        print 'TRACK: ' + track
        stream.filter(track=[track], async=True)
        return stream

    def get_base_directory_path(self):
        return os.getcwd() + '/Twitter_Utils/data/tweets/' + self.game_name_to_store

    def get_base_file_path(self):
        return os.getcwd() + '/Twitter_Utils/data/tweets/' + self.game_name_to_store + '/' + self.game_name_to_store + '.txt'

    def save_tweet_to_disk(self, tweet):
        if not os.path.exists(self.get_base_directory_path()):
            os.makedirs(self.get_base_directory_path())

        with open(self.get_base_file_path(), 'a+b') as f:
            f.write(tweet)
            f.write('\n')
        f.close()
