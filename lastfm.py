import requests
import urllib

BASE_URL = 'http://ws.audioscrobbler.com/2.0'

class LastFm(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def top_artists(self, username, period='6month'):
        return requests.get('%(base_url)s/?method=user.gettopartists&format=json&%(query)s' % \
          {'base_url': BASE_URL,
           'query': urllib.urlencode(
            {'api_key': self._api_key,
             'user': username,
             'period': period})}).json()['topartists']['artist']
