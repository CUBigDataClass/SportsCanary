import json
import os
import unittest
import datetime
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
        fo = open(path, 'w')
        fo.write('[{"uuid": "4b2fb0bc-864c-4ede-be61-59ed14e1da50", "title": "Spurs vs Clippers",'
                 '"start_time": "2016-02-18T17:18:00-08:00", "being_streamed": true, "home_team_id":'
                 '"5bf2300f-777b-4caa-9ef3-3fda11f17ad1", "away_team_id": "ed803cc0-8e6e-4798-b5aa-9eecbc977801",'
                 '"slug": "nba-2015-2016-sa-lac-2016-02-18-1930"}]')
        fo.close()
        # register remove function
        self.addCleanup(os.remove, path)

    def test_check_if_stream_should_end(self):
        # Shouldn't end if there is no stream
        self.assertEqual(False, self.eternalProcess.check_if_stream_should_end())
        # Should end if there is a stream
        self.eternalProcess.end_times_list.append(datetime.datetime.now().strftime('%H:%M'))
        stream = self.data_gatherer.get_tweet_stream('ok', '123', '123')
        self.eternalProcess.stream_list.append(stream)
        self.assertEqual(True, self.eternalProcess.check_if_stream_should_end())

    def test_get_time_to_end_stream(self):
        eternal_process = EternalProcess()
        now = datetime.datetime.now()
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
        eternal_process.sleep_for(1)
        time_now_plus_1 = datetime.datetime.now().strftime('%H:%M:%S')
        time_now += datetime.timedelta(seconds=1)
        time_now = time_now.strftime('%H:%M:%S')
        self.assertEqual(time_now, time_now_plus_1)

    def test_update_is_streamed_json(self):
        eternal_process = EternalProcess()
        eternal_process.update_is_streamed_json(0)
        path = self.eternalProcess.base_path + self.time_now.strftime('%Y-%m-%d') + '.json'
        json_file = open(path, 'r')
        data = json.load(json_file)
        self.assertEqual(True, data[0]['being_streamed'])

    def test_update_is_streamed_throws_error(self):
        eternal_process = EternalProcess()
        eternal_process.base_path = ''
        with self.assertRaises(IOError):
            eternal_process.update_is_streamed_json(0)
        assert True

    def test_create_keyword_string_for_game(self):
        eternal_process = EternalProcess()
        game = {'home_team_id': '20901970-53a0-417c-b5b4-832a74148af6',
                'away_team_id': '1c65bbb6-bd10-4ef6-831a-89050d57fe16'}
        expected = eternal_process.create_keyword_string_for_game(game)
        self.assertEqual(expected, 'TrueToAtlanta,TrueToAtlanta,ATL,Hawks,goTrueToAtlanta,goTrueToAtlanta,goATL'
                                   ',goHawks,Celtics,Celtics,Celtics,goCeltics,goCeltics,goCeltics')

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
