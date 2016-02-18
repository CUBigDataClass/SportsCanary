import urllib2
import socks
from sockshandler import SocksiPyHandler


class ProxyHandler:
    """This proxy only works from certain IP's so we might have to find another one or just set it to the server ip"""
    def __init__(self):
        self.proxy_ip = '213.184.104.219'
        self.proxy_port = 42310

    def url_request(self):
        return urllib2.build_opener(SocksiPyHandler(socks.SOCKS5, self.proxy_ip, self.proxy_port))

