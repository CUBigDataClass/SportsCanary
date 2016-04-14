import unittest
from Eternal_Utils.WebsiteInteraction import WebsiteInteraction


class TestWebsiteInteraction(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_post_request_to_sports_canary(self):
        website_interaction = WebsiteInteraction()
        r = website_interaction.post_request_to_sports_canary(event_name='Test vs Game', score_1=0, score_2=0,
                                                              score_applicable=True, stattleship_slug='mlb-test-123',
                                                              sport_type='mlb',
                                                              team_1_percentage_win=34, team_2_percentage_win=66,
                                                              team_1_name='Test_1', team_2_name='Test_2')
        self.id = website_interaction.id
        t = website_interaction.delete_request_to_sports_canary()
        self.assertEqual(200, r)
        self.assertEqual(200, t)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
