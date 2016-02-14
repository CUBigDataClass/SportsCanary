from twython import TwythonStreamer


class DataGatherer(TwythonStreamer):
    """Class to gather data from Twitter"""

    def on_success(self, data):
        if 'text' in data and 'user' in data:
            print("ID: " + str(data['user']['id']))
            print("Tweet: " + data['text'].encode('utf-8'))

    def on_error(self, status_code, data):
        print status_code
        self.disconnect()
