import unittest
from time import sleep

from Eternal_Utils.Timer import Timer


class TestTimer(unittest.TestCase):
    def test___enter__(self):
        timer = Timer()
        self.assertIsNotNone(timer.__enter__().start)

    def test___exit__(self):
        timer = Timer(True)
        timer.__enter__()
        sleep(0.5)
        timer.__exit__()
        self.assertEqual(0, int(timer.secs))

    def test___init__(self):
        assert True

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
