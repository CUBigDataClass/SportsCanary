import unittest
from Twitter_Utils.MarchMadness import MarchMadness


class TestMarchMadness(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_create_keyword_stream(self):
        march_madness = MarchMadness()
        self.assertEqual('none', march_madness.create_keyword_stream())

    def test_get_march_madness_games_for_the_day(self):
        march_madness = MarchMadness()
        self.assertEqual([], march_madness.get_march_madness_games_for_the_day())

    def test_return_games_for_the_day(self):
        march_madness = MarchMadness()
        self.assertEqual([], march_madness.return_games_for_the_day())

    def test_write_days_games_data(self):
        march_madness = MarchMadness()
        self.assertEqual(True, march_madness.write_days_games_data())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()