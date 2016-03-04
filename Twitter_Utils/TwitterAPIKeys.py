import os


class TwitterAPIKeyHandler:
    def __init__(self):
        self.api_key_array = []
        self.number_of_keys = 2

    def get_api_keys_from_environment(self):
        """
        Gets all API keys we have saved to our environment.
        :return: returns an array of individual dictionary entries with key info.
        """
        for key in range(0, self.number_of_keys):
            app_key = 'TWITTER_APP_KEY_' + str(key)
            app_secret = 'TWITTER_APP_SECRET_' + str(key)
            oauth_token = 'TWITTER_OAUTH_TOKEN_' + str(key)
            oauth_token_secret = 'TWITTER_OAUTH_TOKEN_SECRET_' + str(key)

            app_key = os.environ[app_key]
            app_secret = os.environ[app_secret]
            oauth_token = os.environ[oauth_token]
            oauth_token_secret = os.environ[oauth_token_secret]

            individual_key = dict(app_key=app_key,
                                  app_secret=app_secret,
                                  oauth_token=oauth_token,
                                  oauth_token_secret=oauth_token_secret)
            self.api_key_array.append(individual_key)

        return self.api_key_array
