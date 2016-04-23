import unittest
from Gambling_Utils.OddsConversion import american_to_decimal, decimal_to_american


class TestAmericanToDecimal(unittest.TestCase):
    def test_american_to_decimal(self):
        expected = 2.2
        self.assertEqual(expected, american_to_decimal(120))
        expected = 1.833
        self.assertEqual(expected, american_to_decimal(-120))


class TestDecimalToAmerican(unittest.TestCase):
    def test_decimal_to_american(self):
        expected = 212.0
        self.assertEqual(expected, decimal_to_american(3.12))
        expected = -125.0
        self.assertEqual(expected, decimal_to_american(1.80))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
