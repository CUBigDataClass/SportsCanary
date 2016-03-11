import unittest
from Eternal_Utils.SetupLogging import setup_logging


class TestSetupLogging(unittest.TestCase):
    def test_setup_logging(self):
        self.assertEqual(True, setup_logging())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
