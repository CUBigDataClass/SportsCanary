import unittest
from Gambling_Utils import BetFairAPI


class TestOddsGeneration(unittest.TestCase):
    def test___init__(self):
        assert True  # TODO: implement your test here

    def test_call_api(self):
        odds_generation = BetFairAPI.OddsGeneration()
        json_request = event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
        self.assertIsNotNone(odds_generation.call_api(json_request))

    def test_create_urllib2_request(self):
        odds_generation = BetFairAPI.OddsGeneration()
        session_key_headers = odds_generation.set_session_key_headers()
        data = odds_generation.set_data_for_session()
        session_key_url = odds_generation.set_session_key_url()
        odds_generation.create_urllib2_request(session_key_url, data, session_key_headers)
        assert True

    def test_get_event_type_id_given_name(self):
        odds_generation = BetFairAPI.OddsGeneration()
        self.assertEqual('7522', odds_generation.get_event_type_id_given_name('Basketball'))

    # def test_get_event_types(self):
    #     # odds_generation = OddsGeneration()
    #     # self.assertEqual(expected, odds_generation.get_event_types())
    #     assert True  # TODO: implement your test here

    def test_get_session_key_and_set_headers(self):
        odds_generation = BetFairAPI.OddsGeneration()
        result = odds_generation.get_session_key_and_set_headers()
        self.assertIsNot(False, result)

    def test_set_data_for_session(self):
        odds_generation = BetFairAPI.OddsGeneration()
        odds_generation.BET_FAIR_USERNAME = 'fred'
        odds_generation.BET_FAIR_PASSWORD = 'loh'
        expected = 'username=' + 'fred' + '&password=' + 'loh'
        self.assertEqual(expected, odds_generation.set_data_for_session())

    def test_set_session_key_headers(self):
        odds_generation = BetFairAPI.OddsGeneration()
        odds_generation.APP_KEY_DELAYED = ''
        expected = {
            'Accept': 'application/json',
            'X-Application': ''
        }
        self.assertEqual(expected, odds_generation.set_session_key_headers())

    def test_set_session_key_url(self):
        odds_generation = BetFairAPI.OddsGeneration()
        expected = 'https://identitysso.betfair.com/api/login'
        self.assertEqual(expected, odds_generation.set_session_key_url())

    def test_set_session_token_and_api_call_headers(self):
        # odds_generation = OddsGeneration()
        # self.assertEqual(expected, odds_generation.set_session_token_and_api_call_headers(json_response))
        assert True # TODO: implement your test here

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
