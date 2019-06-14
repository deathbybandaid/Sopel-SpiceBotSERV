# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to search google"""

import requests
from fake_useragent import UserAgent


class Google():

    def __init__(self):
        self.cache = {
                    "info": {},
                    "maps": {}
                    }

    def search(self, searchterm, searchtype="info"):

        # losercase searching
        searchterm = searchterm.lower()

        # check cache
        if searchtype not in list(self.cache.keys()):
            self.cache[searchtype] = dict()
        if searchterm in self.cache[searchtype]:
            return self.cache[searchtype][searchterm]

        header = {'User-Agent': str(UserAgent().chrome)}
        data = searchterm.replace(' ', '+')
        lookfor = data.replace(':', '%3A')
        try:
            if searchtype == 'maps':
                var = requests.get(r'http://www.google.com/maps/place/' + lookfor, headers=header)
            elif searchtype == 'info':
                var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI', headers=header)
            else:
                var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI', headers=header)
        except Exception as e:
            var = e
            var = None

        if not var or not var.url:
            return None
        else:
            self.cache[searchtype][searchterm] = str(var.url)
            return var.url


google = Google()