import requests
import json
import urllib
import time

BASE_URL = 'http://api.musicgraph.com/api/v2'

class MusicGraph(object):
    __name__ = 'musicgraph'

    def __init__(self, api_key):
        self._api_key = api_key

    def gender(self, artist):
        """Given an artist name, return their gender ('male', 'female',
        'both' for mixed-gender bands, 'other' or None if unknown).
        """
        artistname = artist.encode('utf-8')
        r = requests.get('%(base_url)s/artist/search?api_key=%(api_key)s&limit=1&%(query)s' \
            % {'base_url': BASE_URL, 'api_key': self._api_key,
                'query': urllib.urlencode({'name': artistname})})
        j = r.json()
        if 'data' in j and len(j['data']) > 0 and 'gender' in j['data'][0]:
            return j['data'][0]['gender'].lower()
        else:
            return None
