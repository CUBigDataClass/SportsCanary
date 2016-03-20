import unittest
from Twitter_Utils.MarchMadness import MarchMadness


class TestMarchMadness(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_create_keyword_stream(self):
        # march_madness = MarchMadness()
        # self.assertEqual(expected, march_madness.create_keyword_stream())
        assert True # TODO: implement your test here

    def test_get_march_madness_games_for_the_day(self):
        march_madness = MarchMadness()
        # self.assertIsNotNone(march_madness.get_march_madness_games_for_the_day())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()