import re
import random
import requests
import itertools
from lxml.html import fromstring
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class FreeProxy(object):
    def __init__(self,input):
        self.choice=input
        
    def freeproxylist(self):
          freeurl = 'https://free-proxy-list.net/anonymous-proxy.html'
          freeresponse = requests.get(freeurl, verify=False)
          freeparser = fromstring(freeresponse.text)
          freeproxies = []
          for i in freeparser.xpath('//tbody/tr')[:10]:
              if i.xpath('.//td[7][contains(text(),"yes")]'):
                  freeproxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
              try:
                  t = requests.get("https://www.google.com/", proxies={"http": freeproxy, "https": freeproxy}, timeout=5)
                  if t.status_code == requests.codes.ok:
                      freeproxies.append(freeproxy)
              except:
                  pass
          return freeproxies

    def proxyparse(self, proxy):
        proxy_parts = proxy.split(':')
        if len(proxy_parts) == 2:
            ip, port = proxy_parts
            formatted_proxy = {
                'http': f'http://{ip}:{port}/',
            }
            auth=None
        elif len(proxy_parts) == 4:
            ip, port, user, password = proxy_parts
            formatted_proxy = {
                'http': f'http://{user}:{password}@{ip}:{port}/',
            }
            auth=None
        formatted_proxy = formatted_proxy['http']
        return formatted_proxy, auth

    def __repr__(self):
        freeproxy = self.freeproxylist()
        random_pick=random.choice(freeproxy)
        if self.choice == 'url':
            proxylink,auth=self.proxyparse(random_pick)
        else:
            proxylink=random_pick
        return proxylink

class PaidProxy(object):
    def __init__(self, filepath):
        self.filepath=filepath

    def readproxy(self,input):
        with open(input) as txt_file:
            proxies = txt_file.read().splitlines()
        return proxies

    def __repr__(self):
        proxies =self.readproxy(self.filepath)
        proxy_swm = itertools.cycle(proxies)
        proxy = next(proxy_swm)
        fp=FreeProxy()
        proxyurl, httpauth = fp.proxyparse(proxy)
        return proxyurl
