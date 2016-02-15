from DataGatherer import DataGatherer
from EternalProcess import EternalProcess
import os

APP_KEY = os.environ['TWITTER_APP_KEY']
APP_SECRET = os.environ['TWITTER_APP_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']

if __name__ == "__main__":
    # data_gather = DataGatherer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    # data_gather.get_tweet_stream('gowest,goeast,go east,go west,#nbaallstarto,allstars,all stars')
    process = EternalProcess()
    process.start_process()
