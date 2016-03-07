import unittest
from Eternal_Utils import CommonUtils


class TestCommonUtils(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_get_environ_variable(self):
        common_utils = CommonUtils.CommonUtils()
        expected = common_utils.get_environ_variable('BET_FAIR_USERNAME')
        self.assertEqual('johnbd1', expected)

    def test_get_environ_variable_except(self):
        common_utils = CommonUtils.CommonUtils()
        self.assertEqual('Test_Case', common_utils.get_environ_variable('Test_Cases_Coverage'))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
