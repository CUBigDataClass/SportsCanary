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
from TwitterClient import TwitterClient
from Eternal_Utils.CommonUtils import CommonUtils
from Eternal_Utils.WebsiteInteraction import WebsiteInteraction
from sys import platform as _platform
from MarchMadness import MarchMadness
from Eternal_Utils.ScoreUpdater import ScoreUpdater


class EternalProcess:
    def __init__(self):
        self.sports_data = SportsData()
        self.keyword_generator = KeywordGenerator()
        self.march_madness = MarchMadness()
        self.score_updater = ScoreUpdater()
        self.website_interaction = WebsiteInteraction()
        self.twitter_client = TwitterClient()
        self.tick_time_in_seconds = 60.0
        self.time_prior_to_game_to_start_stream = 180
        self.time_to_check_games_for_the_day = '02:00'
        self.time_to_update_scores_for_the_day = '02:00'
        self.time_to_clear_api_keys = '02:00'
        self.data_gatherer = DataGatherer()
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos + 15]
        else:
            path = wd
        self.base_path = path + '/Twitter_Utils/data/daily-logs/'
        self.stream_list = []
        self.end_times_list = []
        self.game_name_list = []
        self.slug_list = []
        self.logger = logging.getLogger(__name__)
        if _platform == "linux" or _platform == "linux2":
            handler = logging.handlers.SysLogHandler('/dev/log')
            # add formatter to the handler
            formatter = logging.Formatter('Python: { "loggerName":"%(name)s", "asciTime":"%(asctime)s",'
                                          '"pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f",'
                                          '"functionName":"%(funcName)s", "levelNo":"%(levelno)s",'
                                          '"lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s",'
                                          '"message":"%(message)s"}')
            handler.formatter = formatter
            self.logger.addHandler(handler)

    def start_process(self):  # pragma: no cover
        """
        This process is our workhorse, it has to check if it should log games.
        It has to check if a game is starting and if that is the case, fork the process,
        And in that new process check for game data during the time period assigned to it.
        """
        # self.wait_till_five_seconds_into_minute()
        start_time = time.time()
        print(50 * '*' + '\n' + 10 * '*' + '  STARTING SCANNING PROCESS   ' + 10 * '*' + '\n' + 50 * '*')
        while True:
            self.logger.info('Stream list: ' + str(self.stream_list))
            self.logger.info('Game list: ' + str(self.game_name_list))
            self.logger.info('Slug list: ' + str(self.slug_list))
            self.logger.info('End Times list: ' + str(self.end_times_list))
            self.check_if_stream_should_end()

            if self.is_time_to_get_game_data_for_day():
                self.write_days_games_data_for_nba()
                self.write_days_games_data_for_nhl()
                self.write_days_games_data_for_mlb()

            if self.is_time_to_update_scores_for_day():
                self.score_updater.get_score_and_update_mongo()

            if self.is_time_to_clear_api_keys():
                self.data_gatherer.key_handler.delete_api_keys_file()

            # Read in file to see if it is time to analyze twitter
            read_path = self.get_write_path_for_days_games()

            db = self.get_aws_mongo_db()
            data_nba = []
            data_nhl = []
            data_mlb = []
            for post in db.nba_logs.find():
                if post['date'] == datetime.datetime.now().strftime('%Y-%m-%d'):
                    data_nba.append(post)

            for post in db.nhl_logs.find():
                if post['date'] == datetime.datetime.now().strftime('%Y-%m-%d'):
                    data_nhl.append(post)

            for post in db.mlb_logs.find():
                if post['date'] == datetime.datetime.now().strftime('%Y-%m-%d'):
                    data_mlb.append(post)

            data_mm = self.march_madness.return_games_for_the_day()

            try:
                with open(read_path):
                    current_time = self.get_time_as_hour_minute()
                    self.logger.info('Current Time: ' + current_time)
                    self.logger.info('--------------------')
                    self.iterate_through_daily_games_and_start_stream(data=data_nba, current_time=current_time,
                                                                      sport="nba")
                    self.logger.info('--------------------')
                    self.iterate_through_daily_games_and_start_stream(data=data_nhl, current_time=current_time,
                                                                      sport="nhl")
                    self.logger.info('--------------------')
                    self.iterate_through_daily_games_and_start_stream(data=data_mlb, current_time=current_time,
                                                                      sport="mlb")
                    self.logger.info('--------------------')
                    self.iterate_through_march_madness_games_and_start_stream(data_mm=data_mm,
                                                                              current_time=current_time)

            except IOError:
                self.logger.error('File not found at ' + read_path)
                self.write_days_games_data_for_nhl()
                self.write_days_games_data_for_mlb()
                self.write_days_games_data_for_nba()
                continue

            self.sleep_for(self.tick_time_in_seconds, start_time)

    @staticmethod
    def get_time_as_hour_minute():
        return datetime.datetime.now().strftime('%H:%M')

    def generate_stream_start_time(self, game):
        """
        Given a game returns time to start stream prior to game
        :param game: Game object form Stattleship API
        :return: returns game time as Hour:Minute
        """
        game_time = dateutil.parser.parse(game['start_time']) - \
                    datetime.timedelta(minutes=self.time_prior_to_game_to_start_stream)
        return game_time.strftime('%H:%M')

    def iterate_through_march_madness_games_and_start_stream(self, data_mm, current_time):  # pragma: no cover
        for idx, game in enumerate(data_mm):
            game_time = self.generate_stream_start_time(game)
            self.logger.info('March Madness Game Time: ' + game_time)
            if game_time == current_time and not game['being_streamed']:
                self.march_madness.update_is_streamed_json(game)
                self.logger.info('Acquiring twitter data for ' + str(game["title"]))

                keyword_string = self.march_madness.create_keyword_stream()
                self.start_stream_with_keywords(keyword_string, game)
                return True

    def iterate_through_daily_games_and_start_stream(self, data, current_time, sport):
        for idx, game in enumerate(data):
            # print(game[''])
            game_time = self.generate_stream_start_time(game)
            self.logger.info(sport.upper() + ' Game Time: ' + game_time)
            # if game_time == current_time and not game['being_streamed']:
            if game_time == current_time:
                self.update_is_streamed_json(game, sport)
                self.logger.info('Acquiring twitter data for ' + str(game["title"]))

                keyword_string = self.create_keyword_string_for_game(game, sport)
                self.start_stream_with_keywords(keyword_string, game)

    def start_stream_with_keywords(self, keyword_string, game):
        game_name = self.create_game_name_from_title(game)
        self.game_name_list.append(game_name)
        self.slug_list.append(game['slug'])
        data_gatherer = DataGatherer()
        stream = data_gatherer.get_tweet_stream(keyword_string, game['_id'], game_name)
        self.stream_list.append(stream)
        self.end_times_list.append(
            self.get_time_to_end_stream(self.time_prior_to_game_to_start_stream))

    @staticmethod
    def create_game_name_from_title(game):
        return datetime.datetime.now().strftime('%Y-%m-%d') + '-' + game['title'].replace(' ', '-')

    def wait_till_five_seconds_into_minute(self):
        self.logger.info('Waiting till five seconds into minute to start.')
        while True:
            current_time = datetime.datetime.now().strftime('%S')
            if current_time == '05':
                return True

    def create_keyword_string_for_game(self, game, sport):
        """
        create string of keywords to pass into twitter filter.
        :param sport: currently "nba" or "nhl"
        :param game: game data, contains home and away team id
        :return: string of keywords
        """
        search_terms_home = self.keyword_generator.generate_search_terms(game['home_team_id'], sport)
        search_terms_away = self.keyword_generator.generate_search_terms(game['away_team_id'], sport)
        keyword_string_home = ','.join(search_terms_home)
        keyword_string_away = ','.join(search_terms_away)
        return keyword_string_home + '---' + keyword_string_away

    def update_is_streamed_json(self, game, sport):
        """
        Replaces json file to reflect that game is being streamed
        :param sport: Sport in short hand, currently "nba" or "nhl"
        :param game: game data, containing _id of game to be updated
        """
        try:
            game_id = game["_id"]
            db = self.get_aws_mongo_db()

            if not game['being_streamed']:
                if sport == "nba":
                    db.nba_logs.update({'_id': game_id}, {"$set": {"being_streamed": True}}, upsert=False)
                    return True
                elif sport == "nhl":
                    db.nhl_logs.update({'_id': game_id}, {"$set": {"being_streamed": True}}, upsert=False)
                    return True
                elif sport == "mlb":
                    db.mlb_logs.update({'_id': game_id}, {"$set": {"being_streamed": True}}, upsert=False)
                    return True
            else:
                if sport == "nba":
                    db.nba_logs.update({'_id': game_id}, {"$set": {"being_streamed": False}}, upsert=False)
                    return False
                elif sport == "nhl":
                    db.nhl_logs.update({'_id': game_id}, {"$set": {"being_streamed": False}}, upsert=False)
                    return False
                elif sport == "mlb":
                    db.mlb_logs.update({'_id': game_id}, {"$set": {"being_streamed": True}}, upsert=False)
                    return False
        except:
            print 'error'

    @staticmethod
    def get_aws_mongo_db():
        """
        Connects to AWS hosted MongoDB
        :return: MongoDB instance with database
        """
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        return client.eventsDB

    @staticmethod
    def get_time_to_end_stream(minutes):
        """
        Creates a time to end stream, currently in minutes
        :param minutes:
        :return: Time object
        """
        time_now = datetime.datetime.now()
        now_plus_10 = time_now + datetime.timedelta(minutes=minutes)
        return now_plus_10.strftime('%H:%M')

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
        game_path = self.get_game_name_base_file_path(i)
        team_path_tuple = self.get_team_name_base_file_path(i)

        team_tweet_counts = self.get_tweet_count_per_team(i)

        if team_tweet_counts:
            teams_tuple = self.get_teams_in_game_tuple(i)
            team_tweet_percentages = self.get_percentage_from_two_inputs(team_tweet_counts[0], team_tweet_counts[1])

            self.website_interaction.post_request_to_sports_canary(
                event_name=self.get_game_name_in_team1_vs_team2_format(i),
                score_1=0,
                score_2=0,
                score_applicable=True,
                stattleship_slug=self.slug_list[i],
                sport_type=str(self.slug_list[i])[:3],
                team_1_percentage_win=team_tweet_percentages[0],
                team_2_percentage_win=team_tweet_percentages[1],
                team_1_name=teams_tuple[0],
                team_2_name=teams_tuple[1]
            )

            self.twitter_client.enriched_tweet_based_on_confidence(tweet_percentage_tuple=team_tweet_percentages,
                                                                   teams_tuple=teams_tuple, slug=self.slug_list[i],
                                                                   sport=str(self.slug_list[i])[:3])

        # map_reduced_tweets_game = self.map_reduce_tweets_after_disconnect(game_path, i)
        # map_reduced_tweets_team1 = self.map_reduce_tweets_after_disconnect(team_path_tuple[0], i)
        # map_reduced_tweets_team2 = self.map_reduce_tweets_after_disconnect(team_path_tuple[1], i)
        #
        # self.replace_written_tweets_with_map_reduced_version_for_uncategorized_tweets(i, map_reduced_tweets_game)
        # self.replace_written_tweets_with_map_reduced_version_for_teams(team_path_tuple[0], map_reduced_tweets_team1)
        # self.replace_written_tweets_with_map_reduced_version_for_teams(team_path_tuple[1], map_reduced_tweets_team2)

        # self.remove_first_line_from_file(self.get_game_name_base_file_path(i))
        # self.remove_first_line_from_file(team_path_tuple[0])
        # self.remove_first_line_from_file(team_path_tuple[1])

        self.delete_stream_end_time_game_name_from_lists(i)

        if not self.check_if_stream_should_end():
            return True

    @staticmethod
    def get_percentage_from_two_inputs(team_1_tweet_count, team_2_tweet_count):
        """
        Given two counts returns tuple of percentages
        :param team_1_tweet_count: Int of tweet amount
        :param team_2_tweet_count: Int of tweet amount
        :return: Tuple of two ints in % form
        """
        total_tweet_count = team_1_tweet_count + team_2_tweet_count
        team_1_percentage = int(float((float(team_1_tweet_count) / float(total_tweet_count)) * 100))
        team_2_percentage = int(float((float(team_2_tweet_count) / float(total_tweet_count)) * 100))
        return team_1_percentage, team_2_percentage

    def get_tweet_count_per_team(self, i):
        """
        Gets number of tweets for each team
        :param i: index
        :return: tuple of counts
        """
        try:
            team_path_tuple = self.get_team_name_base_file_path(i)
            with open(team_path_tuple[0]) as f:
                for i, l in enumerate(f):
                    pass
            team1_count = i + 1

            with open(team_path_tuple[1]) as fx:
                for i, l in enumerate(fx):
                    pass
            team2_count = i + 1
            return team1_count, team2_count

        except IOError:
            return False

    def delete_stream_end_time_game_name_from_lists(self, i):
        """
        Deletes entry for stream, end_times, and game name lists.
        :param i: index at which to clear
        """
        try:
            del self.stream_list[i]
            del self.end_times_list[i]
            del self.game_name_list[i]
            del self.slug_list[i]
        except IndexError:
            raise IndexError

    def get_index_and_clear_api_key_at_index(self, idx):
        """
        Get index from index_stream tuple and clear the api key at index
        :param idx: index at which to get tuple from list
        """
        index_stream = self.stream_list[idx]
        index = index_stream[1]
        return self.data_gatherer.key_handler.clear_api_key_at_index_for_use(index)

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

    def is_time_to_update_scores_for_day(self):
        """
        :return: checks if its time to update our mongodb with scores for the day and returns BOOL
        """
        if self.time_to_update_scores_for_the_day == datetime.datetime.now().strftime('%H:%M'):
            return True
        else:
            return False

    def is_time_to_clear_api_keys(self):
        """
        :return: checks if its time to clear api keys and returns BOOL
        """
        if self.time_to_clear_api_keys == datetime.datetime.now().strftime('%H:%M'):
            return True
        else:
            return False

    def map_reduce_tweets_after_disconnect(self, game_path, index):
        # TODO - Currently breaks if list has no repeated tweets
        """
        Uses Popen to open and pipe 5 processes, in order to MapReduce tweets
        :param index:
        :param game_path:
        :return: returns object of newly map reduced tweets
        """
        try:
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

        except ValueError:
            self.logger.exception(ValueError)
            self.logger.error('Map Reduce Value Error')

    def replace_written_tweets_with_map_reduced_version_for_uncategorized_tweets(self, index, map_reduced_tweets):
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

    def replace_written_tweets_with_map_reduced_version_for_teams(self, file_path, map_reduced_tweets):
        """
        Opens tweets file and replaces it with map reduced version
        :param file_path:
        :param map_reduced_tweets: map_reduced_tweets object to be written
        """
        try:
            with open(file_path, 'w+') as f:
                f.write(map_reduced_tweets)
            f.close()
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found to map reduce for team 1.')
            print 'IOError'

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

    def get_game_name_in_team1_vs_team2_format(self, index):
        """
        Creates Team_1 vs Team_2 string from ex. 2016-03-01-Hawks-vs-Warriors
        :param index: index at game_name_list
        :return: concatenated string
        """
        game_name = self.game_name_list[index]
        split_str = game_name.split('-')
        vs_index = split_str.index('vs')
        team1_name, team2_name = split_str[vs_index - 1], split_str[vs_index + 1]
        return str(team1_name) + ' vs ' + str(team2_name)

    def get_teams_in_game_tuple(self, index):
        """
        Given a Team_1 vs Team_2 returns a tuple of Team_1, Team_2
        :param index: index at game_name_list
        :return: tuple of team names in string format
        """
        game_name = self.game_name_list[index]
        split_str = game_name.split('-')
        vs_index = split_str.index('vs')
        team1_name, team2_name = split_str[vs_index - 1], split_str[vs_index + 1]
        return str(team1_name), str(team2_name)

    def get_team_name_base_file_path(self, index):
        try:
            game_name = self.game_name_list[index]
            split_str = game_name.split('-')
            vs_index = split_str.index('vs')
            team1_name, team2_name = split_str[vs_index - 1], split_str[vs_index + 1]
            wd = os.getcwd()
            pos = wd.find("BigDataMonsters")
            if pos > 0:  # pragma: no cover
                path = wd[0:pos + 15]
            else:
                path = wd
            return path + '/Twitter_Utils/data/tweets/' + game_name + '/' + team1_name + '.txt', \
                   path + '/Twitter_Utils/data/tweets/' + game_name + '/' + team2_name + '.txt'
        except IndexError:
            print 'IndexError while getting team name base file path.'
        except IOError:
            print 'IOError while getting team name base file path.'

    # TODO - Figure out how to test this
    def write_days_games_data_for_nba(self):
        """
        Writes API response containing info for days games in the NBA
        """
        db = self.get_aws_mongo_db()
        write_path = self.get_write_path_for_days_games()
        data_to_write = self.sports_data.get_games_for_today_for_sport("nba")
        try:
            with open(write_path, 'w+') as f:
                f.write(data_to_write)
            f.close()
            with open(write_path) as data_file:
                data = json.load(data_file)
            db.nba_logs.insert(data)
            return True
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('Unable to write at ' + write_path)
            raise IOError
        except:
            self.logger.error('Unable to write days data for nba, due to data existing already.')
            return False

    def write_days_games_data_for_nhl(self):
        """
        Writes API response containing info for days games in the NHL
        """
        db = self.get_aws_mongo_db()
        write_path = self.get_write_path_for_days_games()
        data_to_write = self.sports_data.get_games_for_today_for_sport("nhl")
        try:
            with open(write_path, 'w+') as f:
                f.write(data_to_write)
            f.close()
            with open(write_path) as data_file:
                data = json.load(data_file)
            db.nhl_logs.insert(data)
            return True
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('Unable to write at ' + write_path)
            raise IOError
        except:
            self.logger.error('Unable to write days data for nhl, due to data existing already.')
            return False

    def write_days_games_data_for_mlb(self):
        """
        Writes API response containing info for days games in the MLB
        """
        db = self.get_aws_mongo_db()
        write_path = self.get_write_path_for_days_games()
        data_to_write = self.sports_data.get_games_for_today_for_sport("mlb")
        try:
            with open(write_path, 'w+') as f:
                f.write(data_to_write)
            f.close()
            with open(write_path) as data_file:
                data = json.load(data_file)
            db.mlb_logs.insert(data)
            return True

        except IOError:
            self.logger.exception(IOError)
            self.logger.error('Unable to write at ' + write_path)
            raise IOError

        except:
            self.logger.error('Unable to write days data for mlb, due to data existing already.')
            return False

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
            return True
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found at ' + path)
            return False

    def remove_last_line_from_file(self, path):
        """
        Removes last line from file
        :param path: path to file
        """
        try:
            with open(path, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(path, 'w') as fout:
                fout.writelines(data[:-1])
                fout.close()
            return True
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found at ' + path)
            return False

    @staticmethod
    def sleep_for(tick_time_in_seconds, start_time):
        """
        Sleeps for number of seconds required to start at next minute tick.
        :param start_time: start time
        :param tick_time_in_seconds: seconds to sleep for
        """
        time.sleep(tick_time_in_seconds - ((time.time() - start_time) % tick_time_in_seconds))
