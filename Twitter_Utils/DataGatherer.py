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
        self.home_team_file_path = ''
        self.away_team_file_path = ''
        self.common_file_path = ''
        self.dir_path = ''
        self.home_team_track_words = ''
        self.away_team_track_words = ''

    def get_auth(self):
        index = self.key_handler.check_which_key_to_use()
        if index is not None:
            self.auth = OAuthHandler(self.key_array[index]['app_key'], self.key_array[index]['app_secret'])
            self.auth.set_access_token(self.key_array[index]['oauth_token'],
                                       self.key_array[index]['oauth_token_secret'])
            return index
        else:
            self.logger.info('No key found, stream not started.')

    def on_error(self, status_code):
        self.logger.error('Error: ' + str(status_code))
        # returning False in on_data disconnects the stream
        return False

    def on_status(self, status):  # pragma: no cover
        if status.lang == 'en':
            processed_tweet = self.processor.standardize_tweet(status.text)
            if any(word in status.text.lower() for word in self.home_team_track_words.lower().split(',')):
                self.save_tweet_to_disk(processed_tweet, self.home_team_file_path)
            elif any(word in status.text.lower() for word in self.away_team_track_words.lower().split(',')):
                self.save_tweet_to_disk(processed_tweet, self.away_team_file_path)
            else:
                self.save_tweet_to_disk(processed_tweet, self.common_file_path)

    def get_tweet_stream(self, track, game_id, game_name):
        index = self.get_auth()
        self.logger.info('Using auth: ' + str(self.auth.consumer_key))
        print(track)
        print(game_id)
        print(game_name)
        self.set_paths(track, game_id, game_name)
        stream = Stream(self.auth, self)
        stream.filter(track=[track], async=True)
        return stream, index

    def set_paths(self, track, game_id, game_name):
        self.game_id_to_store = game_id
        self.game_name_to_store = game_name
        self.logger.info('Track: ' + str(track))
        self.home_team_track_words, self.away_team_track_words = track.split('---')
        self.set_base_directory_path()
        split_str = game_name.split('-')
        vs_index = split_str.index('vs')
        team1_name, team2_name = split_str[vs_index-1], split_str[vs_index+1]
        if team1_name in self.home_team_track_words:
            self.set_base_file_path(team1_name, team2_name, game_name)
        elif team1_name in self.away_team_track_words:
            self.set_base_file_path(team2_name, team1_name, game_name)
        else:
            self.logger.error('Error: Team name not matching keywords.  Team 1: ' + team1_name +
                              '. Team 2: ' + team2_name)

    def set_base_directory_path(self):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        self.dir_path = path + '/Twitter_Utils/data/tweets/' + self.game_name_to_store
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    def set_base_file_path(self, home_file_name, away_file_name, game_name):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        self.home_team_file_path = self.dir_path + '/' + home_file_name + '.txt'
        self.away_team_file_path = self.dir_path + '/' + away_file_name + '.txt'
        self.common_file_path = self.dir_path + '/' + game_name + '.txt'

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

    @staticmethod
    def save_tweet_to_disk(tweet, file_path):
        with open(file_path, 'a+b') as f:
            f.write(tweet)
            f.write('\n')
        f.close()

    @staticmethod
    def create_feature_vector(tweet):
        feature_vector = []
        words = tweet.split()
        for word in words:
            feature_vector.append(word)

        return feature_vector
