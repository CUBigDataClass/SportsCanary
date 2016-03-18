from TweetProcessing import TweetProcessor
from TwitterAPIKeySwitcher import TwitterAPIKeyHandler
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from Eternal_Utils.CommonUtils import CommonUtils
import os
import logging


class DataGatherer(StreamListener):
    """
    Class responsible for spawning twitter streams and storing tweets.
    Twitter Streaming API: https://dev.twitter.com/streaming/overview/request-parameters#track
    """
    def __init__(self):
        super(DataGatherer, self).__init__()
        self.APP_KEY = CommonUtils.get_environ_variable('TWITTER_APP_KEY')
        self.APP_SECRET = CommonUtils.get_environ_variable('TWITTER_APP_SECRET_0')
        self.OAUTH_TOKEN = CommonUtils.get_environ_variable('TWITTER_OAUTH_TOKEN_0')
        self.OAUTH_TOKEN_SECRET = CommonUtils.get_environ_variable('TWITTER_OAUTH_TOKEN_SECRET_0')
        self.processor = TweetProcessor()
        self.key_handler = TwitterAPIKeyHandler()
        self.key_array = self.key_handler.get_api_keys_from_environment()
        self.game_id_to_store = ''
        self.game_name_to_store = ''
        self.auth = OAuthHandler(self.APP_KEY, self.APP_SECRET)
        self.auth.set_access_token(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
        self.api = API(self.auth)
        self.logger = logging.getLogger(__name__)

    def get_auth(self):
        index = self.key_handler.check_which_key_to_use()
        if index is not None:
            self.auth = OAuthHandler(self.key_array[index]['app_key'], self.key_array[index]['app_secret'])
            self.auth.set_access_token(self.key_array[index]['oauth_token'],
                                       self.key_array[index]['oauth_token_secret'])
            return index
        else:
            raise Exception

    def on_error(self, status_code):
        self.logger.error('Error: ' + str(status_code))
        # returning False in on_data disconnects the stream
        return False

    def on_status(self, status):  # pragma: no cover
        if status.lang == 'en':
            processed_tweet = self.processor.standardize_tweet(status.text)
            self.save_tweet_to_disk(processed_tweet)

    def get_tweet_stream(self, track, game_id, game_name):
        index = self.get_auth()
        self.logger.info('Using auth: ' + str(self.auth.consumer_key))
        stream = Stream(self.auth, self)
        self.game_id_to_store = game_id
        self.game_name_to_store = game_name
        self.logger.info('Track: ' + str(track))
        stream.filter(track=[track], async=True)
        return stream, index

    def get_base_directory_path(self):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        return path + '/Twitter_Utils/data/tweets/' + self.game_name_to_store

    def get_base_file_path(self):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        return path + '/Twitter_Utils/data/tweets/' + self.game_name_to_store + '/' + self.game_name_to_store + '.txt'

    # TODO - Figure out how to test
    def save_tweet_to_disk(self, tweet):  # pragma: no cover
        if not os.path.exists(self.get_base_directory_path()):
            os.makedirs(self.get_base_directory_path())

        with open(self.get_base_file_path(), 'a+b') as f:
            f.write(tweet)
            f.write('\n')
        f.close()
