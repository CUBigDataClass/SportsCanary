import json
import os
import unittest
import datetime
import time
from Twitter_Utils.EternalProcess import EternalProcess
from Twitter_Utils.DataGatherer import DataGatherer
from Eternal_Utils.CommonUtils import CommonUtils
from Twitter_Utils.TwitterAPIKeySwitcher import TwitterAPIKeyHandler
from pymongo import MongoClient


class TestEternalProcess(unittest.TestCase):
    def test___init__(self):
        assert True

    def setUp(self):
        self.eternalProcess = EternalProcess()
        self.stream_list = []
        self.end_times_list = []
        self.time_to_check_games_for_the_day = '09:30'
        self.data_gatherer = DataGatherer()

        self.time_now = datetime.datetime.now()
        path = self.eternalProcess.base_path + self.time_now.strftime('%Y-%m-%d') + '.json'
        fo = open(path, 'w+')
        fo.write('[{"uuid": "4b2fb0bc-864c-4ede-be61-59ed14e1da50", "title": "Spurs vs Clippers",'
                 '"start_time": "2016-02-18T17:18:00-08:00", "being_streamed": true, "home_team_id":'
                 '"5bf2300f-777b-4caa-9ef3-3fda11f17ad1", "away_team_id": "ed803cc0-8e6e-4798-b5aa-9eecbc977801",'
                 '"slug": "nba-2015-2016-sa-lac-2016-02-18-1930"}]')
        fo.close()
        # register remove function
        self.addCleanup(os.remove, path)

        dir_path = os.getcwd() + '/Twitter_Utils/data/tweets/base_tweets_for_tests'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        self.addCleanup(os.rmdir, dir_path)
        self.path_2 = os.getcwd() + '/Twitter_Utils/data/tweets/base_tweets_for_tests/base_tweets_for_tests.txt'
        fo = open(self.path_2, 'w+')
        fo.write('test tweet 1\ntest tweet 1\ntest tweet 1\ntest tweet 1\ntest tweet 2\ntest tweet 2\ntest tweet 2\n')
        fo.close()
        self.addCleanup(os.remove, self.path_2)

    def test_check_if_stream_should_end(self):
        # Shouldn't end if there is no stream
        self.assertEqual(False, self.eternalProcess.check_if_stream_should_end())
        # Should end if there is a stream
        self.eternalProcess.end_times_list.append(datetime.datetime.now().strftime('%H:%M'))
        self.eternalProcess.game_name_list.append('2016-03-05-Pacers-vs-Wizards')
        keywords = 'TrueToAtlanta,TrueToAtlanta,ATL,Hawks,DennisSchroder,ThaboSefolosha,' \
                   'TimHardawayJr.,PaulMillsap,MikeScott,JeffTeague,MikeMuscala,KyleKorver,' \
                   'AlHorford,KentBazemore,goTrueToAtlanta,goTrueToAtlanta,goATL,goHawks,' \
                   'goDennisSchroder,goThaboSefolosha,goTimHardawayJr.,goPaulMillsap,goMikeScott,' \
                   'goJeffTeague,goMikeMuscala,goKyleKorver,goAlHorford,goKentBazemore,' \
                   'Dennis Schroder,Thabo Sefolosha,Tim Hardaway Jr.,Paul Millsap,Mike Scott,' \
                   'Jeff Teague,Mike Muscala,Kyle Korver,Al Horford,Kent Bazemore' \
                   '---Celtics,Celtics,Celtics,CotyClarke,IsaiahThomas,JamesYoung,AveryBradley,' \
                   'TerryRozier,EvanTurner,JordanMickey,MarcusSmart,JaredSullinger,KellyOlynyk,' \
                   'TylerZeller,R.J.Hunter,AmirJohnson,JonasJerebko,goCeltics,goCeltics,goCeltics,' \
                   'goCotyClarke,goIsaiahThomas,goJamesYoung,goAveryBradley,goTerryRozier,goEvanTurner,' \
                   'goJordanMickey,goMarcusSmart,goJaredSullinger,goKellyOlynyk,goTylerZeller,' \
                   'goR.J.Hunter,goAmirJohnson,goJonasJerebko,Coty Clarke,Isaiah Thomas,James Young,' \
                   'Avery Bradley,Terry Rozier,Evan Turner,Jordan Mickey,Marcus Smart,Jared Sullinger,' \
                   'Kelly Olynyk,Tyler Zeller,R.J. Hunter,Amir Johnson,Jonas Jerebko'

        stream = self.data_gatherer.get_tweet_stream(keywords, '123', '2016-03-05-Pacers-vs-Wizards')
        self.eternalProcess.stream_list.append(stream)
        self.eternalProcess.slug_list.append('nbae-slugerino-123')
        self.assertEqual(True, self.eternalProcess.check_if_stream_should_end())

    def test_check_if_stream_should_end_should_return_false_if_none(self):
        now = datetime.datetime.now()
        now_plus_10 = now + datetime.timedelta(minutes=10)
        now_plus_10 = now_plus_10.strftime('%H:%M')
        self.eternalProcess.end_times_list.append(now_plus_10)
        self.assertEqual(False, self.eternalProcess.check_if_stream_should_end())

    def test_get_time_to_end_stream(self):
        now = datetime.datetime.now()
        eternal_process = EternalProcess()
        now_plus_10 = now + datetime.timedelta(minutes=10)
        now_plus_10 = now_plus_10.strftime('%H:%M')
        self.assertEqual(now_plus_10, eternal_process.get_time_to_end_stream(10))

    def test_get_write_path_for_days_games(self):
        eternal_process = EternalProcess()
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos+15]
        else:
            path = wd
        base = path + '/Twitter_Utils/data/daily-logs/'
        end = datetime.datetime.now().strftime('%Y-%m-%d') + '.json'
        self.assertEqual(base + end, eternal_process.get_write_path_for_days_games())

    def test_is_time_to_get_game_data_for_day(self):
        eternal_process = EternalProcess()
        eternal_process.time_to_check_games_for_the_day = datetime.datetime.now().strftime('%H:%M')
        self.assertEqual(True, eternal_process.is_time_to_get_game_data_for_day())
        eternal_process.time_to_check_games_for_the_day = '04:14'
        self.assertEqual(False, eternal_process.is_time_to_get_game_data_for_day())

    def test_sleep_for(self):
        eternal_process = EternalProcess()
        time_now = datetime.datetime.now()
        eternal_process.sleep_for(1, time.time())
        time_now_plus_1 = datetime.datetime.now().strftime('%H:%M:%S')
        time_now += datetime.timedelta(seconds=1)
        time_now = time_now.strftime('%H:%M:%S')
        self.assertEqual(time_now, time_now_plus_1)

    def test_map_reduce_tweets_after_disconnect(self):
        self.eternalProcess.game_name_list.append('123')
        path = self.eternalProcess.get_game_name_base_file_path(0)
        self.assertIsNotNone(self.eternalProcess.map_reduce_tweets_after_disconnect(path, 0))

    def test_get_game_name_base_file_path(self):
        self.eternalProcess.game_name_list.append('2016-03-05-Pacers-vs-Wizards')
        self.assertEqual(os.getcwd() + '/Twitter_Utils/data/tweets/2016-03-05-Pacers-vs-Wizards/'
                                       '2016-03-05-Pacers-vs-Wizards.txt',
                         self.eternalProcess.get_game_name_base_file_path(0))

    def test_delete_stream_end_time_game_name_from_lists(self):
        eternal_process = EternalProcess()
        eternal_process.stream_list.append('Stream Test')
        eternal_process.end_times_list.append('End Time Test')
        eternal_process.game_name_list.append('Game Test')
        eternal_process.slug_list.append('nbae-Slug-mlb-123')
        self.assertIs(len(eternal_process.stream_list), 1)
        self.assertIs(len(eternal_process.end_times_list), 1)
        self.assertIs(len(eternal_process.game_name_list), 1)
        eternal_process.delete_stream_end_time_game_name_from_lists(0)
        self.assertIs(len(eternal_process.stream_list), 0)
        self.assertIs(len(eternal_process.end_times_list), 0)
        self.assertIs(len(eternal_process.game_name_list), 0)

    def test_get_game_name_directory(self):
        eternal_process = EternalProcess()
        eternal_process.game_name_list.append('Test_game')
        expected = 'Twitter_Utils/data/tweets/Test_game/'
        self.assertEqual(expected, eternal_process.get_game_name_directory(0))

    def test_remove_first_line_from_file(self):
        eternal_process = EternalProcess()
        path = os.getcwd() + '/Twitter_Utils/data/tweets/base_tweets_for_tests/base_tweets_for_tests.txt'
        count_1 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_1 += 1
        reader.close()
        self.assertIs(True, eternal_process.remove_first_line_from_file(path))
        count_2 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_2 += 1
        reader.close()

        self.assertEqual(count_1-1, count_2)

    def test_remove_first_line_from_file_raises_ioerror(self):
        eternal_process = EternalProcess()
        path = os.getcwd() + '/Twitter_Utils/data/tweets/not_a_real_path/not_a_real_path.txt'
        self.assertIs(False, eternal_process.remove_first_line_from_file(path))

    def test_remove_last_line_from_file_raises_ioerror(self):
        eternal_process = EternalProcess()
        path = os.getcwd() + '/Twitter_Utils/data/tweets/not_a_real_path/not_a_real_path.txt'
        self.assertIs(False, eternal_process.remove_last_line_from_file(path))

    def test_remove_last_line_from_file(self):
        eternal_process = EternalProcess()
        path = os.getcwd() + '/Twitter_Utils/data/tweets/base_tweets_for_tests/base_tweets_for_tests.txt'
        count_1 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_1 += 1
        reader.close()
        self.assertIs(True, eternal_process.remove_last_line_from_file(path))
        count_2 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_2 += 1
        reader.close()
        self.assertEqual(count_1-1, count_2)

    def test_create_game_name_from_title(self):
        eternal_process = EternalProcess()
        game = {'title': 'Test vs Cases'}
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        expected = date + '-Test-vs-Cases'
        self.assertEqual(expected, eternal_process.create_game_name_from_title(game))

    def test_get_aws_mongo_db(self):
        eternal_process = EternalProcess()
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        expected = client.eventsDB
        self.assertEqual(expected, eternal_process.get_aws_mongo_db())

    def test_get_time_as_hour_minute(self):
        eternal_process = EternalProcess()
        self.assertEqual(datetime.datetime.now().strftime('%H:%M'), eternal_process.get_time_as_hour_minute())

    def test_wait_till_five_seconds_into_minute(self):
        eternal_process = EternalProcess()
        self.assertEqual(True, eternal_process.wait_till_five_seconds_into_minute())
        current_time = datetime.datetime.now().strftime('%S')
        self.assertEqual(current_time, '05')

    def test_write_days_games_data_for_nba(self):
        eternal_process = EternalProcess()
        self.assertIsNotNone(eternal_process.write_days_games_data_for_nba())

    def test_write_days_games_data_for_nhl(self):
        eternal_process = EternalProcess()
        self.assertIsNotNone(eternal_process.write_days_games_data_for_nhl())

    def test_create_keyword_string_for_game(self):
        eternal_process = EternalProcess()
        game = {'home_team_id': '84eb19ca-1e66-416f-9e00-90b20fe4bb5e',
                'away_team_id': '68b04d26-12c3-4e06-8ae0-5bab39686213'}
        sport = 'nba'
        self.assertGreater(len(eternal_process.create_keyword_string_for_game(game, sport)), 35)

    def test_generate_stream_start_time(self):
        eternal_process = EternalProcess()
        game = {'start_time': '2016-03-17T19:00:00-06:00'}
        expected = '16:00'
        self.assertEqual(expected, eternal_process.generate_stream_start_time(game))

    def test_get_index_and_clear_api_key_at_index(self):
        eternal_process = EternalProcess()
        twitter_key_handler = TwitterAPIKeyHandler()
        test_stream = 'test stream', 0
        eternal_process.stream_list.append(test_stream)
        self.assertEqual(False, eternal_process.get_index_and_clear_api_key_at_index(0))
        with open(twitter_key_handler.key_check_write_path) as f:
            data = json.load(f)
        twitter_key_handler.update_json_file(data, 0)
        test_stream = 'test stream', 0
        eternal_process.stream_list.append(test_stream)
        self.assertEqual(True, eternal_process.get_index_and_clear_api_key_at_index(0))

    def test_get_team_name_base_file_path(self):
        eternal_process = EternalProcess()
        # ExpectedNone
        self.assertIsNone(eternal_process.get_team_name_base_file_path(0))
        eternal_process.game_name_list.append('Cavaliers-vs-Bronx')

        expected = os.getcwd() + '/Twitter_Utils/data/tweets/Cavaliers-vs-Bronx/Cavaliers-vs-Bronx.txt'
        self.assertEqual(expected, eternal_process.get_game_name_base_file_path(0))

    def test_iterate_through_daily_games_and_start_stream(self):
        eternal_process = EternalProcess()
        start_time = datetime.datetime.now() + datetime.timedelta(minutes=180)
        data = [{'start_time': str(start_time), 'being_streamed': False, '_id': 'fak31D',
                 'title': 'Cavaliers vs Mavericks',
                 'home_team_id': 'a9abb922-3a47-4d37-9250-2e5224a2b58a',
                 'away_team_id': '35ded680-b7b1-4cd9-a223-7bc4ab0b77ed',
                 'slug': 'nba-slug-mlb-123'}]
        current_time = eternal_process.get_time_as_hour_minute()
        eternal_process.iterate_through_daily_games_and_start_stream(data, current_time, "nba")
        self.assertEqual(1, len(eternal_process.game_name_list))
        self.assertIs(True, eternal_process.end_stream_and_free_api(0))

    def test_update_is_streamed_json(self):
        eternal_process = EternalProcess()
        game = dict(_id='f334b7d4-a1fb-4ed6-ad85-ba75f71f0b1f', being_streamed=False)
        sport = 'nba'
        self.assertEqual(True, eternal_process.update_is_streamed_json(game, sport))
        game = dict(_id='f334b7d4-a1fb-4ed6-ad85-ba75f71f0b1f', being_streamed=True)
        self.assertEqual(False, eternal_process.update_is_streamed_json(game, sport))

    def test_get_game_name_in_team1_vs_team2_format(self):
        eternal_process = EternalProcess()
        eternal_process.game_name_list.append('2016-03-18-Warriors-vs-Oilers')
        self.assertEqual('Warriors vs Oilers', eternal_process.get_game_name_in_team1_vs_team2_format(0))

    def test_write_days_games_data_for_mlb(self):
        eternal_process = EternalProcess()
        self.assertIsNotNone(eternal_process.write_days_games_data_for_mlb())

    def test_get_percentage_from_two_inputs(self):
        eternal_process = EternalProcess()
        self.assertEqual((25, 75), eternal_process.get_percentage_from_two_inputs(10, 30))

    def test_get_teams_in_game_tuple(self):
        eternal_process = EternalProcess()
        eternal_process.game_name_list.append('2016-04-13-Test-vs-Game')
        self.assertEqual(('Test','Game'), eternal_process.get_teams_in_game_tuple(0))

    def test_is_time_to_clear_api_keys(self):
        eternal_process = EternalProcess()
        if datetime.datetime.now().strftime('%H:%M') == '02:00':
            self.assertEqual(True, eternal_process.is_time_to_clear_api_keys())
        else:
            self.assertEqual(False, eternal_process.is_time_to_clear_api_keys())

    def test_is_time_to_update_scores_for_day(self):
        eternal_process = EternalProcess()
        if datetime.datetime.now().strftime('%H:%M') == '02:00':
            self.assertEqual(True, eternal_process.is_time_to_update_scores_for_day())
        else:
            self.assertEqual(False, eternal_process.is_time_to_update_scores_for_day())
if __name__ == '__main__':  # pragma: no cover
    unittest.main()
