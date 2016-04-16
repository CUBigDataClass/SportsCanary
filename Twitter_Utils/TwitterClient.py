from Eternal_Utils.CommonUtils import CommonUtils
from Eternal_Utils.ScoreUpdater import ScoreUpdater
from Twitter_Utils.KeywordGenerator import KeywordGenerator
import tweepy


class TwitterClient:
    def __init__(self):
        """
        Initializes API keys and sets up Auth with Twitter API
        """
        self.APP_KEY = CommonUtils.get_environ_variable('SPORTS_CANARY_APP_KEY')
        self.APP_SECRET = CommonUtils.get_environ_variable('SPORTS_CANARY_APP_KEY_SECRET')
        self.OAUTH_TOKEN = CommonUtils.get_environ_variable('SPORTS_CANARY_OAUTH_TOKEN')
        self.OAUTH_TOKEN_SECRET = CommonUtils.get_environ_variable('SPORTS_CANARY_OAUTH_TOKEN_SECRET')
        self.auth = tweepy.OAuthHandler(self.APP_KEY, self.APP_SECRET)
        self.auth.set_access_token(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.keyword_generator = KeywordGenerator()
        self.score_updater = ScoreUpdater()

    def tweet(self, tweet):
        """
        Tweets out content
        :param tweet: message to be tweeted
        """
        self.api.update_status(tweet)

    def delete_latest_tweet(self):
        timeline = self.api.user_timeline(count=1)
        for t in timeline:
            self.api.destroy_status(t.id)

    def take_data_gathering_input(self, tweet_percentage_tuple, game_name, teams_tuple, slug, sport):
        'We predict that the TEAM1 will be victorious today against the TEAM2. #SPORT #hashtags'
        pass


# if team_tweet_percentages[0] > team_tweet_percentages[1]:
#     self.twitter_client.tweet('We predict that in ' + self.get_game_name_in_team1_vs_team2_format(i) +
#                               ', ' + teams_tuple[0] + ' will be victorious.')
# else:
#     self.twitter_client.tweet('We predict that in ' + self.get_game_name_in_team1_vs_team2_format(i) +
#                               ', ' + teams_tuple[1] + ' will be victorious.')