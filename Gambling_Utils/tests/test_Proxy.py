import unittest
from Gambling_Utils import Proxy


class TestProxyHandler(unittest.TestCase):
    def test___init__(self):
        # proxy_handler = ProxyHandler()
        assert True  # TODO: implement your test here

    def test_url_request(self):
        proxy_handler = Proxy.ProxyHandler()
        proxy_handler.url_request()
        assert True  # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
