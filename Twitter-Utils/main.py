from DataGatherer import DataGatherer
import os

APP_KEY = os.environ['TWITTER_APP_KEY']
APP_SECRET = os.environ['TWITTER_APP_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']

if __name__ == "__main__":
    stream = DataGatherer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track='Superbowl, SB50')
