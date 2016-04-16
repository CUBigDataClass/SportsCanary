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

    def take_data_gathering_input(self, tweet_percentage_tuple, teams_tuple, slug, sport):
        home_away_id_tuple = self.score_updater.get_team_ids_for_game(slug, sport)
        home_hashtags = self.keyword_generator.get_hashtags_for_team(team_id=home_away_id_tuple[0])
        home_hashtags = ['#' + hashtag for hashtag in home_hashtags]
        home_hashtags = ' '.join(home_hashtags)
        away_hashtags = self.keyword_generator.get_hashtags_for_team(team_id=home_away_id_tuple[1])
        away_hashtags = ['#' + hashtag for hashtag in away_hashtags]
        away_hashtags = ' '.join(away_hashtags)
        if tweet_percentage_tuple[0] > tweet_percentage_tuple[1]:
            if abs(tweet_percentage_tuple[0] - tweet_percentage_tuple[1]) <= 15:
                self.tweet('We predict that the' + teams_tuple[0] + ' will be victorious today against the ' +
                           teams_tuple[1] + '. #' + sport.upper() + ' ' + home_hashtags + ' ' + away_hashtags)
            else:
                self.tweet('We feel confident that the' + teams_tuple[0] + ' will be victorious today against the ' +
                           teams_tuple[1] + '. #' + sport.upper() + ' ' + home_hashtags + ' ' + away_hashtags)
        else:
            if abs(tweet_percentage_tuple[1] - tweet_percentage_tuple[0]) <= 15:
                self.tweet('We predict that the' + teams_tuple[1] + ' will be victorious today against the ' +
                           teams_tuple[0] + '. #' + sport.upper() + ' ' + home_hashtags + ' ' + away_hashtags)
            else:
                self.tweet('We feel confident that the' + teams_tuple[1] + ' will be victorious today against the ' +
                           teams_tuple[0] + '. #' + sport.upper() + ' ' + home_hashtags + ' ' + away_hashtags)
