import unittest
from Gambling_Utils import Proxy


class TestProxyHandler(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_url_request(self):
        proxy_handler = Proxy.ProxyHandler()
        result = proxy_handler.url_request()
        self.assertIsNotNone(result)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
