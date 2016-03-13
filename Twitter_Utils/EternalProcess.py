import time
import datetime
import dateutil.parser
import os
import json
import logging
import logging.handlers
from pymongo import MongoClient
from subprocess import Popen, PIPE
from SportsData import SportsData
from DataGatherer import DataGatherer
from KeywordGenerator import KeywordGenerator
from Eternal_Utils.CommonUtils import CommonUtils
from sys import platform as _platform


class EternalProcess:
    def __init__(self):
        self.sports_data = SportsData()
        self.keyword_generator = KeywordGenerator()
        self.tick_time_in_seconds = 60.0
        self.time_prior_to_game_to_start_stream = 125
        self.time_to_check_games_for_the_day = '16:34'
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
        self.logger = logging.getLogger(__name__)
        if _platform == "linux" or _platform == "linux2":
            handler = logging.handlers.SysLogHandler('/dev/log')
            # add formatter to the handler
            formatter = logging.Formatter('Python: { "loggerName":"%(name)s", "asciTime":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')
            handler.formatter = formatter
            self.logger.addHandler(handler)

    def start_process(self):  # pragma: no cover
        """
        This process is our workhorse, it has to check if it should log games.
        It has to check if a game is starting and if that is the case, fork the process,
        And in that new process check for game data during the time period assigned to it.
        """
        start_time = time.time()
        print(50 * '*' + '\n' + 10 * '*' + '  STARTING SCANNING PROCESS   ' + 10 * '*' + '\n' + 50 * '*')
        while True:
            self.logger.info('Stream list: ' + str(self.stream_list))
            self.logger.info('End Times list: ' + str(self.end_times_list))
            self.check_if_stream_should_end()
            # TODO - If stream ends, map reduce tweets, then analyze them.
            if self.is_time_to_get_game_data_for_day():
                self.write_days_games_data()

            # Read in file to see if it is time to analyze twitter
            read_path = self.get_write_path_for_days_games()

            uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
            client = MongoClient(uri)
            db = client.eventsDB
            data = []
            for post in db.nba_logs.find():
                if post['date'] == datetime.datetime.now().strftime('%Y-%m-%d'):
                    data.append(post)

            try:
                with open(read_path) as f:
                    # data = json.load(f)
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    self.logger.info('Current Time: ' + current_time)
                    for idx, game in enumerate(data):
                        game_time = dateutil.parser.parse(game['start_time']) - \
                                    datetime.timedelta(minutes=self.time_prior_to_game_to_start_stream)
                        game_time = game_time.strftime('%H:%M')
                        self.logger.info('Game Time: ' + game_time)

                        if game_time == current_time and not game['being_streamed']:
                            self.update_is_streamed_json(index=idx, game=game)
                            self.logger.info('Acquiring twitter data for ' + str(game["title"]))

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
                self.logger.exception(IOError)
                self.logger.error('File not found at ' + read_path)
                self.write_days_games_data()
                # raise IOError

            self.sleep_for(self.tick_time_in_seconds, start_time)

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

    def update_is_streamed_json(self, index, game):
        """
        Replaces json file to reflect that game is being streamed
        :param index: index within JSON object
        """
        game_id = game["_id"]
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        db = client.eventsDB

        time_now = datetime.datetime.now()
        read_path = self.base_path + time_now.strftime('%Y-%m-%d') + '.json'
        try:
            json_file = open(read_path, 'r')
            data = json.load(json_file)
            json_file.close()
            if not game['being_streamed']:
                # data[index]['being_streamed'] = True
                db.nba_logs.update({'_id':game_id}, {"$set": {"being_streamed": True}}, upsert=False)
            else:
                # data[index]['being_streamed'] = False
                db.nba_logs.update({'_id':game_id}, {"$set": {"being_streamed": False}}, upsert=False)

            json_file = open(read_path, 'w+')
            json_file.write(json.dumps(data))
            json_file.close()

        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found at ' + read_path)
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

    # TODO - Fairly certain this will not end two streams that are supposed to end at the same time
    def check_if_stream_should_end(self):
        """
        Runs through active streams and if its time to end it, ends it and clears the api key for use
        :return: returns True if stream has been ended, if there is no stream then it returns False
        """
        if self.end_times_list:
            hour_min_time_now = datetime.datetime.now().strftime('%H:%M')
            # TODO - Refactor the line below this
            for i in xrange(len(self.end_times_list) - 1, -1, -1):
                if self.end_times_list[i] == hour_min_time_now:
                    return self.end_stream_and_free_api(i)
            return False
        else:
            return False

    def end_stream_and_free_api(self, i):
        """
        Clears api key, disconnects stream, map reduces tweets, removes first line and deletes entries from lists
        :param i: index at which to clear keys, streams and everything
        :return: True Bool, have to catch exceptions
        """
        self.get_index_and_clear_api_key_at_index(i)
        self.get_and_disconnect_stream_at_index(i)
        map_reduced_tweets = self.map_reduce_tweets_after_disconnect(i)
        self.replace_written_tweets_with_map_reduced_version(i, map_reduced_tweets)
        self.remove_first_line_from_file(self.get_game_name_base_file_path(i))
        self.delete_stream_end_time_game_name_from_lists(i)
        return True

    def delete_stream_end_time_game_name_from_lists(self, i):
        """
        Deletes entry for stream, end_times, and game name lists.
        :param i: index at which to clear
        """
        try:
            del self.stream_list[i]
            del self.end_times_list[i]
            del self.game_name_list[i]
        except KeyError:
            raise KeyError

    def get_index_and_clear_api_key_at_index(self, idx):
        """
        Get index from index_stream tuple and clear the api key at index
        :param idx: index at which to get tuple from list
        """
        index_stream = self.stream_list[idx]
        index = index_stream[1]
        self.data_gatherer.key_handler.clear_api_key_at_index_for_use(index)

    def get_and_disconnect_stream_at_index(self, idx):
        """
        Get stream from index_stream tuple and clear stream
        :param idx: index at which to get tuple from list
        """
        index_stream = self.stream_list[idx]
        stream = index_stream[0]
        self.logger.info('Stream List ' + str(self.stream_list))
        self.logger.info('Stopping ' + str(stream))
        stream.disconnect()

    def get_write_path_for_days_games(self):
        """
        :return: base path for days games from Stattleship API
        """
        return self.base_path + datetime.datetime.now().strftime('%Y-%m-%d') + '.json'

    def is_time_to_get_game_data_for_day(self):
        """
        :return: checks if its time to get data and returns BOOL
        """
        if self.time_to_check_games_for_the_day == datetime.datetime.now().strftime('%H:%M'):
            return True
        else:
            return False

    def map_reduce_tweets_after_disconnect(self, index):
        # TODO - Currently breaks if list has no repeated tweets
        """
        Uses Popen to open and pipe 5 processes, in order to MapReduce tweets
        :param index: index for get_game_name_directory
        :return: returns object of newly map reduced tweets
        """
        try:
            game_path = self.get_game_name_base_file_path(index)
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
            return map_reduced_tweets

        except IndexError:
            self.logger.exception(IndexError)
            self.logger.error('Map Reduce error at index ' + index)
            raise IOError

    def replace_written_tweets_with_map_reduced_version(self, index, map_reduced_tweets):
        """
        Opens tweets file and replaces it with map reduced version
        :param index: index for get_game_name_base_file_path
        :param map_reduced_tweets: map_reduced_tweets object to be written
        """
        try:
            with open(self.get_game_name_base_file_path(index), 'w+') as f:
                f.write(map_reduced_tweets)
            f.close()
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found at ' + self.get_game_name_base_file_path(index))
            print 'IOError'
            # TODO - Raise IOError
            # raise IOError

    def get_game_name_directory(self, index):
        """
        Gets directory given index for game_name_list
        :param index:
        :return: path to game_name.txt
        """
        game_name = self.game_name_list[index]
        return 'Twitter_Utils/data/tweets/' + game_name + '/'

    def get_game_name_base_file_path(self, index):
        """
        Gets file given index for game_name_list
        :param index:
        :return: path to game_name.txt
        """
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
        """
        Writes API response containing info for days games
        """
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        db = client.eventsDB
        write_path = self.get_write_path_for_days_games()
        data_to_write = self.sports_data.get_nba_games_for_today()
        try:
            with open(write_path, 'w+') as f:
                f.write(data_to_write)
            f.close()
            with open(write_path) as data_file:
                data = json.load(data_file)
            db.nba_logs.insert(data)
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('Unable to write at ' + write_path)
            raise IOError

    def remove_first_line_from_file(self, path):
        """
        Removes first line from file
        :param path: path to file
        """
        try:
            with open(path, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(path, 'w') as fout:
                fout.writelines(data[1:])
                fout.close()
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found at ' + path)
            print 'IOError'
            # TODO - Raise IOError
            # raise IOError

    @staticmethod
    def remove_last_line_from_file(path):
        """
        Removes last line from file
        :param path: path to file
        """
        with open(path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(path, 'w') as fout:
            fout.writelines(data[:-1])
            fout.close()

    @staticmethod
    def sleep_for(tick_time_in_seconds, start_time):
        """
        Sleeps for number of seconds required to start at next minute tick.
        :param start_time: start time
        :param tick_time_in_seconds: seconds to sleep for
        """
        time.sleep(tick_time_in_seconds - ((time.time() - start_time) % tick_time_in_seconds))
