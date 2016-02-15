from DataGatherer import DataGatherer
from EternalProcess import EternalProcess
import os

APP_KEY = os.environ['TWITTER_APP_KEY']
APP_SECRET = os.environ['TWITTER_APP_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']

if __name__ == "__main__":
    # stream = DataGatherer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    #
    # # Important reading - https://dev.twitter.com/streaming/overview/request-parameters#track
    # stream.statuses.filter(track='gowest,goeast,go east,go west,#nbaallstarto,allstars,all stars')
    process = EternalProcess()
    process.start_process()
