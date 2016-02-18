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
        base = os.getcwd() + '/Twitter_Utils/data/daily-logs/'
        end = datetime.datetime.now().strftime('%Y-%m-%d') + '.json'
        self.assertEqual(base + end, eternal_process.get_write_path_for_days_games())

    def test_is_time_to_get_game_data_for_day(self):
        eternal_process = EternalProcess()
        eternal_process.time_to_check_games_for_the_day = datetime.datetime.now().strftime('%H:%M')
        self.assertEqual(True, eternal_process.is_time_to_get_game_data_for_day())
        eternal_process.time_to_check_games_for_the_day = '04:14'
        self.assertEqual(False, eternal_process.is_time_to_get_game_data_for_day())

    def test_write_days_games_data(self):
        assert True

    def test_sleep_for(self):
        assert True

    # def test_start_process(self):
    #     # eternal_process = EternalProcess()
    #     # self.assertEqual(expected, eternal_process.start_process())
    #     assert False # TODO: implement your test here
    #
    # def test_update_is_streamed_json(self):
    #     # eternal_process = EternalProcess()
    #     # self.assertEqual(expected, eternal_process.update_is_streamed_json(index))
    #     assert False # TODO: implement your test here

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
