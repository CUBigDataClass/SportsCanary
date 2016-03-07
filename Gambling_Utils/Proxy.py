import urllib2
import socks
from sockshandler import SocksiPyHandler


class ProxyHandler:
    def __init__(self):
        self.proxy_ip = 'localhost'
        self.proxy_port = 8123

    def url_request(self):
        return urllib2.build_opener(SocksiPyHandler(socks.SOCKS5, self.proxy_ip, self.proxy_port))
