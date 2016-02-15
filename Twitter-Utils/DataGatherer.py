from twython import TwythonStreamer
from TweetProcessing import TweetProcessor
import os


class DataGatherer(TwythonStreamer):
    """ Class to gather data from Twitter
        Twitter Streaming API: https://dev.twitter.com/streaming/overview/request-parameters#track
    """

    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
        super(DataGatherer, self).__init__(app_key, app_secret, oauth_token, oauth_token_secret)
        self.processor = TweetProcessor()
        self.game_id_to_store = ''
        self.game_name_to_store = ''

    def on_success(self, data):
        """
        Called once every time a tweet is successfully streamed
        :param data: data received from stream
        """
        if 'text' in data and 'user' in data:
            processed_tweet = self.processor.standardize_tweet(data['text'])
            self.save_tweet_to_disk(processed_tweet)

    def on_error(self, status_code, data):
        print status_code
        self._disconnect()

    def _disconnect(self):
        self.disconnect()

    def get_tweet_stream(self, track, game_id, game_name):
        self.game_id_to_store = game_id
        self.game_name_to_store = game_name
        self.statuses.filter(language='en', track=track)

    def get_base_directory_path(self):
        return os.getcwd() + '/Twitter-Utils/data/tweets/' + self.game_name_to_store

    def get_base_file_path(self):
        return os.getcwd() + '/Twitter-Utils/data/tweets/' + self.game_name_to_store + '/' + self.game_name_to_store + '.txt'

    def save_tweet_to_disk(self, tweet):
        if not os.path.exists(self.get_base_directory_path()):
            os.makedirs(self.get_base_directory_path())

        with open(self.get_base_file_path(), 'a+b') as f:
            f.write(tweet)
            f.write('\n')
        f.close()
