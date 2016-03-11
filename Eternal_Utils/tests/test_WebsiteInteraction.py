import unittest
from Eternal_Utils.WebsiteInteraction import WebsiteInteraction


class TestWebsiteInteraction(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_post_request_to_sports_canary(self):
        website_interaction = WebsiteInteraction()
        r = website_interaction.post_request_to_sports_canary('Test_name', 12, 21, True)
        self.id = website_interaction.id
        t = website_interaction.delete_request_to_sports_canary()
        self.assertEqual(200, r)
        self.assertEqual(200, t)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
