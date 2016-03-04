import urllib2
import socks
import requests
from sockshandler import SocksiPyHandler


class ProxyHandler:
    """This proxy only works from certain IP's so we might have to find another one or just set it to the server ip"""
    def __init__(self):
        self.proxy_ip = 'localhost'
        self.proxy_port = 8123

    def url_request(self):
        return urllib2.build_opener(SocksiPyHandler(socks.SOCKS5, self.proxy_ip, self.proxy_port))
