import re
import random
import requests
from lxml.html import fromstring
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Proxy(object):
    def freeproxylist(self):
          freeurl = 'https://free-proxy-list.net/anonymous-proxy.html'
          freeresponse = requests.get(freeurl, verify=False)
          freeparser = fromstring(freeresponse.text)
          freeproxies = []
          for i in freeparser.xpath('//tbody/tr')[:20]:
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
        proxylink,auth=self.proxyparse(random_pick)
        return proxylink
