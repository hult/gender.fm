import requests
import json
import urllib
import time
import sys

BASE_URL = 'http://api.musicgraph.com/api/v2'

class MusicGraph(object):
    __name__ = 'musicgraph'
    _interval = 1.5

    def __init__(self, api_key):
        self._last_call = 0
        self._api_key = api_key

    def gender(self, artist):
        """Given an artist name, return their gender ('male', 'female',
        'both' for mixed-gender bands, 'other' or None if unknown).
        """
        t = time.time()
        s = self._last_call - t + self._interval
        if s > 0:
            print >> sys.stderr, "Sleeping for %.2f" % s
            time.sleep(s)

        artistname = artist.encode('utf-8')
        params = {
            'api_key': self._api_key,
            'limit': '1',
            'name': artistname
        }
        self._last_call = time.time()
        j = requests.get('%(base_url)s/artist/search' \
            % {'base_url': BASE_URL}, params=params).json()
        if 'data' in j and len(j['data']) > 0 and 'gender' in j['data'][0]:
            return j['data'][0]['gender'].lower()
        else:
            return None
