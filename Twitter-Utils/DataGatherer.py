from twython import TwythonStreamer
from TweetProcessing import TweetProcessor


class DataGatherer(TwythonStreamer):
    """Class to gather data from Twitter"""
    processor = TweetProcessor()

    def on_success(self, data):
        """
        Called once every time a tweet is successfully streamed
        :param data: data received from stream
        """
        if 'text' in data and 'user' in data:
            processed_tweet = self.processor.standardize_tweet(data['text'])
            print processed_tweet
            return processed_tweet

    def on_error(self, status_code, data):
        print status_code
        self.disconnect()

    def disconnect(self):
        self.disconnect()
