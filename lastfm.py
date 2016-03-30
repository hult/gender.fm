import requests

class LastFm(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def top_artists(self, username, period='6month'):
        params = {
            'method': 'user.gettopartists',
            'format': 'json',
            'api_key': self._api_key,
            'user': username,
            'period': period
        }
        artists = requests.get('http://ws.audioscrobbler.com/2.0',
            params=params).json()['topartists']['artist']
        for a in artists:
            a['affinity'] = a['playcount']
        return artists
