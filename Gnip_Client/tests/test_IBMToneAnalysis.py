import unittest
from Gnip_Client.IBMToneAnalysis import ToneAnalyzer
from httmock import urlmatch, HTTMock


class TestToneAnalyzer(unittest.TestCase):
    def test___init__(self):
        tone_analyzer = ToneAnalyzer()
        self.assertIsNotNone(tone_analyzer.username)
        self.assertIsNotNone(tone_analyzer.password)

    def test_query_ibm_for_tone(self):
        tone_analyzer = ToneAnalyzer()
        self.assertIsNotNone(tone_analyzer.query_ibm_for_tone('What is the sentiment of a test tweet?'))

    @urlmatch(netloc=r'(.*\.)?gateway\.watsonplatform\.net(.*)')
    def ibm_mock(self):
        return 'fake return'

    def test_query_ibm_for_tone_exception(self):
        tone_analyzer = ToneAnalyzer()
        with HTTMock(self.ibm_mock):
            self.assertIsNone(tone_analyzer.query_ibm_for_tone('Test tweets.'))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
