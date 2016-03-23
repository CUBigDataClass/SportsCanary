import json
import os
import unittest
import datetime
import time
from Twitter_Utils.EternalProcess import EternalProcess
from Twitter_Utils.DataGatherer import DataGatherer


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
        path_2 = os.getcwd() + '/Twitter_Utils/data/tweets/base_tweets_for_tests/base_tweets_for_tests.txt'
        fo = open(path_2, 'w+')
        fo.write('test tweet 1\ntest tweet 1\ntest tweet 1\ntest tweet 1\ntest tweet 2\ntest tweet 2\ntest tweet 2\n')
        fo.close()
        self.addCleanup(os.remove, path_2)

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

    def test_create_keyword_string_for_game(self):
        eternal_process = EternalProcess()
        game = {'home_team_id': '20901970-53a0-417c-b5b4-832a74148af6',
                'away_team_id': '1c65bbb6-bd10-4ef6-831a-89050d57fe16'}
        expected = eternal_process.create_keyword_string_for_game(game, "nba")
        self.assertEqual(expected, 'TrueToAtlanta,TrueToAtlanta,ATL,Hawks,PaulMillsap,MikeMuscala,KentBazemore,'
                                   'MikeScott,TimHardawayJr.,ThaboSefolosha,AlHorford,KyleKorver,DennisSchroder,'
                                   'JeffTeague,goTrueToAtlanta,goTrueToAtlanta,goATL,goHawks,goPaulMillsap,'
                                   'goMikeMuscala,goKentBazemore,goMikeScott,goTimHardawayJr.,goThaboSefolosha,'
                                   'goAlHorford,goKyleKorver,goDennisSchroder,goJeffTeague,Paul Millsap,Mike Muscala,'
                                   'Kent Bazemore,Mike Scott,Tim Hardaway Jr.,Thabo Sefolosha,Al Horford,Kyle Korver,'
                                   'Dennis Schroder,Jeff Teague---Celtics,Celtics,Celtics,EvanTurner,R.J.Hunter,'
                                   'MarcusSmart,JaredSullinger,AmirJohnson,TylerZeller,AveryBradley,JordanMickey,'
                                   'TerryRozier,KellyOlynyk,JonasJerebko,IsaiahThomas,JamesYoung,CotyClarke,goCeltics,'
                                   'goCeltics,goCeltics,goEvanTurner,goR.J.Hunter,goMarcusSmart,goJaredSullinger,'
                                   'goAmirJohnson,goTylerZeller,goAveryBradley,goJordanMickey,goTerryRozier,'
                                   'goKellyOlynyk,goJonasJerebko,goIsaiahThomas,goJamesYoung,goCotyClarke,'
                                   'Evan Turner,R.J. Hunter,Marcus Smart,Jared Sullinger,Amir Johnson,Tyler Zeller,'
                                   'Avery Bradley,Jordan Mickey,Terry Rozier,Kelly Olynyk,Jonas Jerebko,Isaiah Thomas,'
                                   'James Young,Coty Clarke')

    def test_map_reduce_tweets_after_disconnect(self):
        self.eternalProcess.game_name_list.append('123')
        path = self.eternalProcess.get_game_name_base_file_path(0)
        self.assertIsNotNone(self.eternalProcess.map_reduce_tweets_after_disconnect(path, 0))

    def test_start_process(self):
        assert True  # TODO: implement your test here

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
        eternal_process.remove_first_line_from_file(path)
        count_2 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_2 += 1
        reader.close()

        self.assertEqual(count_1-1, count_2)

    def test_remove_last_line_from_file(self):
        eternal_process = EternalProcess()
        path = os.getcwd() + '/Twitter_Utils/data/tweets/base_tweets_for_tests/base_tweets_for_tests.txt'
        count_1 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_1 += 1
        reader.close()
        eternal_process.remove_last_line_from_file(path)
        count_2 = 0
        with open(path, 'r') as reader:
            for _ in reader:
                count_2 += 1
        reader.close()
        self.assertEqual(count_1-1, count_2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
