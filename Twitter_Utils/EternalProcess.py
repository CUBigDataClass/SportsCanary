import time
import datetime
import dateutil.parser
import os
import json
from subprocess import Popen, PIPE
from SportsData import SportsData
from DataGatherer import DataGatherer
from KeywordGenerator import KeywordGenerator
from Eternal_Utils.CommonUtils import CommonUtils


class EternalProcess:
    def __init__(self):
        self.sports_data = SportsData()
        self.keyword_generator = KeywordGenerator()
        self.tick_time_in_seconds = 60.0
        self.time_prior_to_game_to_start_stream = 1
        self.time_to_check_games_for_the_day = '19:42'
        self.data_gatherer = DataGatherer()
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        self.base_path = path + '/Twitter_Utils/data/daily-logs/'
        self.APP_KEY = CommonUtils.get_environ_variable('TWITTER_APP_KEY_0')
        self.APP_SECRET = CommonUtils.get_environ_variable('TWITTER_APP_SECRET_0')
        self.OAUTH_TOKEN = CommonUtils.get_environ_variable('TWITTER_OAUTH_TOKEN_0')
        self.OAUTH_TOKEN_SECRET = CommonUtils.get_environ_variable('TWITTER_OAUTH_TOKEN_SECRET_0')
        self.stream_list = []
        self.end_times_list = []
        self.game_name_list = []

    def start_process(self):  # pragma: no cover
        """
        This process is our workhorse, it has to check if it should log games.
        It has to check if a game is starting and if that is the case, fork the process,
        And in that new process check for game data during the time period assigned to it.
        """
        print 50 * '*' + '\n' + 10 * '*' + '  STARTING SCANNING PROCESS   ' + 10 * '*' + '\n' + 50 * '*'
        while True:
            print str(self.stream_list) + str(self.end_times_list)

            self.check_if_stream_should_end()
            # TODO - If stream ends, map reduce tweets, then analyze them.
            if self.is_time_to_get_game_data_for_day:
                self.write_days_games_data()

            # Read in file to see if it is time to analyze twitter
            read_path = self.get_write_path_for_days_games()

            try:
                with open(read_path) as f:
                    data = json.load(f)
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    print 'Current Time: ' + current_time
                    for idx, game in enumerate(data):
                        game_time = dateutil.parser.parse(game['start_time']) - \
                                    datetime.timedelta(minutes=self.time_prior_to_game_to_start_stream)
                        game_time = game_time.strftime('%H:%M')
                        print 'Game Time: ' + game_time
                        if game_time == current_time and not game['being_streamed']:
                            self.update_is_streamed_json(index=idx)
                            print 'Time to get twitter data.'

                            keyword_string = self.create_keyword_string_for_game(game)

                            game_name = datetime.datetime.now().strftime('%Y-%m-%d') + '-' + game['title'].replace(' ',
                                                                                                                   '-')
                            self.game_name_list.append(game_name)

                            data_gatherer = DataGatherer()
                            stream = data_gatherer.get_tweet_stream(keyword_string, game['uuid'], game_name)
                            self.stream_list.append(stream)
                            self.end_times_list.append(
                                self.get_time_to_end_stream(self.time_prior_to_game_to_start_stream))

            except IOError:
                print 'File not found'

            # restart loop after sleep, given by our tick_time
            self.sleep_for(self.tick_time_in_seconds)

    def create_keyword_string_for_game(self, game):
        """
        create string of keywords to pass into twitter filter.
        :param game: game data, contains home and away team id
        :return: string of keywords
        """
        search_terms_home = self.keyword_generator.generate_search_terms(game['home_team_id'])
        search_terms_away = self.keyword_generator.generate_search_terms(game['away_team_id'])
        keyword_string_home = ','.join(search_terms_home)
        keyword_string_away = ','.join(search_terms_away)
        return keyword_string_home + ',' + keyword_string_away

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
            raise IOError

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
                    stream = stream[0]
                    index = self.stream_list[i]
                    index = index[1]
                    print self.stream_list
                    print 'Stopping: ' + str(stream)
                    stream.disconnect()
                    self.data_gatherer.key_handler.clear_api_key_at_index_for_use(index)
                    map_reduced_tweets = self.map_reduce_tweets_after_disconnect(i)
                    self.replace_written_tweets_with_map_reduced_version(i, map_reduced_tweets)
                    self.remove_first_line_from_file(self.get_game_name_base_file_path(i))
                    del self.stream_list[i]
                    del self.end_times_list[i]
                    del self.game_name_list[i]
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

    def map_reduce_tweets_after_disconnect(self, index):
        # TODO - Currently breaks if list has no repeated tweets
        self.game_name_list.append('2016-03-05-Pacers-vs-Wizards')
        try:
            game_path = self.get_game_name_directory(index)
            p1 = Popen(['cat', game_path], stdout=PIPE)
            p2 = Popen(['python', 'Twitter_Utils/Mapper.py'], stdin=p1.stdout, stdout=PIPE)
            p3 = Popen(['sort'], stdin=p2.stdout, stdout=PIPE)
            p4 = Popen(['python', 'Twitter_Utils/Reducer.py'], stdin=p3.stdout, stdout=PIPE)
            p5 = Popen(['sort', '-n'], stdin=p4.stdout, stdout=PIPE)
            # Allow p1 to receive a SIGPIPE if p2 exits.
            p1.stdout.close()
            p2.stdout.close()
            p3.stdout.close()
            p4.stdout.close()
            map_reduced_tweets = p5.communicate()[0]
            print map_reduced_tweets
            return map_reduced_tweets

        except IndexError:
            print 'List out of range'

    def replace_written_tweets_with_map_reduced_version(self, index, map_reduced_tweets):
        with open(self.get_game_name_base_file_path(index), 'w+') as f:
            f.write(map_reduced_tweets)
        f.close()

    def get_game_name_directory(self, index):
        game_name = self.game_name_list[index]
        return 'Twitter_Utils/data/tweets/' + game_name + '/' + game_name + '.txt'

    def get_game_name_base_file_path(self, index):
        game_name = self.game_name_list[index]
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        return path + '/Twitter_Utils/data/tweets/' + game_name + '/' + game_name + '.txt'

    # TODO - Figure out how to test this
    def write_days_games_data(self):  # pragma: no cover
        write_path = self.get_write_path_for_days_games()
        data_to_write = self.sports_data.get_nba_games_for_today()
        try:
            with open(write_path, 'w+') as f:
                f.write(data_to_write)
            f.close()
        except IOError:
            print 'File not found'

    @staticmethod
    def remove_first_line_from_file(path):
        with open(path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(path, 'w') as fout:
            fout.writelines(data[1:])
            fout.close()

    @staticmethod
    def remove_last_line_from_file(path):
        with open(path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(path, 'w') as fout:
            fout.writelines(data[:-1])
            fout.close()

    @staticmethod
    def sleep_for(tick_time):
        start_time = time.time()
        time.sleep(tick_time - ((time.time() - start_time) % tick_time))
