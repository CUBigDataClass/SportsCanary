import time
import datetime
import dateutil.parser
import os
import json
from SportsData import SportsData
from DataGatherer import DataGatherer
from KeywordGenerator import KeywordGenerator


class EternalProcess:
    def __init__(self):
        self.sports_data = SportsData()
        self.keyword_generator = KeywordGenerator()
        self.tick_time_in_seconds = 60.0
        self.time_to_check_games_for_the_day = '09:30'
        self.base_path = os.getcwd() + '/Twitter_Utils/data/daily-logs/'
        self.APP_KEY = os.environ['TWITTER_APP_KEY']
        self.APP_SECRET = os.environ['TWITTER_APP_SECRET']
        self.OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
        self.OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
        self.stream_list = []
        self.end_times_list = []

    def start_process(self):
        """
        This process is our workhorse, it has to check if it should log games.
        It has to check if a game is starting and if that is the case, fork the process,
        And in that new process check for game data during the time period assigned to it.
        """
        print 50 * '*' + '\n' + 10 * '*' + '  STARTING SCANNING PROCESS   ' + 10 * '*' + '\n' + 50 * '*'

        while True:
            print str(self.stream_list) + str(self.end_times_list)

            self.check_if_stream_should_end()

            if self.is_time_to_get_game_data_for_day:
                self.write_days_games_data()

            # Read in file to see if it is time to analyze twitter
            read_path = self.get_write_path_for_days_games()

            try:
                with open(read_path) as f:
                    data = json.load(f)
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    for idx, game in enumerate(data):
                        game_time = dateutil.parser.parse(game['start_time']).strftime('%H:%M')
                        if game_time == current_time and not game['being_streamed']:
                            # TODO - Figure out how to call a fork or child process for a certain amount of time
                            # TODO - Refactor this
                            self.update_is_streamed_json(index=idx)
                            print 'Time to get twitter data.'

                            search_terms_home = self.keyword_generator.generate_search_terms(game['home_team_id'])
                            search_terms_away = self.keyword_generator.generate_search_terms(game['away_team_id'])
                            keyword_string_home = ','.join(search_terms_home)
                            keyword_string_away = ','.join(search_terms_away)

                            keyword_string = keyword_string_home + ',' + keyword_string_away
                            game_name = datetime.datetime.now().strftime('%Y-%m-%d') + '-' + game['title'].replace(' ', '-')

                            data_gatherer = DataGatherer()
                            stream = data_gatherer.get_tweet_stream(keyword_string, game['uuid'], game_name)
                            self.stream_list.append(stream)
                            self.end_times_list.append(self.get_time_to_end_stream(1))

            except IOError:
                print 'File not found'

            # restart loop after sleep, given by our tick_time
            self.sleep_for(self.tick_time_in_seconds)

    def update_is_streamed_json(self, index):
        """
        Replaces json file to reflect that game is being streamed
        :param index: index within JSON object
        """
        time_now = datetime.datetime.now()
        read_path = self.base_path + time_now.strftime('%Y-%m-%d') + '.json'
        try:
            json_file = open(read_path, 'r')
            data = json.load(json_file)
            json_file.close()

            data[index]['being_streamed'] = True

            json_file = open(read_path, 'w+')
            json_file.write(json.dumps(data))
            json_file.close()
            
        except IOError:
                print 'File not found'

    @staticmethod
    def get_time_to_end_stream(minutes):
        """
        Function creates a time to end stream, currently in minutes
        :param minutes:
        :return: Time object
        """
        time_now = datetime.datetime.now()
        now_plus_10 = time_now + datetime.timedelta(minutes=minutes)
        return now_plus_10.strftime('%H:%M')

    def check_if_stream_should_end(self):
        if self.end_times_list:
            hour_min_time_now = datetime.datetime.now().strftime('%H:%M')
            did_delete = False
            # TODO - Refactor the line below this
            for i in xrange(len(self.end_times_list) - 1, -1, -1):
                if self.end_times_list[i] == hour_min_time_now:
                    stream = self.stream_list[i]
                    print 'Stopping: ' + str(stream)
                    stream.disconnect()
                    del self.stream_list[i]
                    del self.end_times_list[i]
                    did_delete = True

            return did_delete
        else:
            return False

    def get_write_path_for_days_games(self):
        return self.base_path + datetime.datetime.now().strftime('%Y-%m-%d') + '.json'

    def is_time_to_get_game_data_for_day(self):
        if self.time_to_check_games_for_the_day == datetime.datetime.now().strftime('%H:%M'):
            return True
        else:
            return False

    def write_days_games_data(self):
        write_path = self.get_write_path_for_days_games()
        data_to_write = self.sports_data.get_nba_games_for_today()
        try:
            with open(write_path, 'w+') as f:
                f.write(data_to_write)
            f.close()
        except IOError:
            print 'File not found'

    @staticmethod
    def sleep_for(tick_time):
        start_time = time.time()
        time.sleep(tick_time - ((time.time() - start_time) % tick_time))
