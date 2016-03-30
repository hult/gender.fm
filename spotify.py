import requests
import urllib

BASE_URL = 'https://api.spotify.com/v1'

class Spotify(object):
    def __init__(self, access_token):
        self._access_token = access_token

    def top_artists(self, time_range='medium_term'):
        headers = { 'Authorization': 'Bearer ' + self._access_token }
        params = {'time_range': time_range}
        artists = requests.get('%(base_url)s/me/top/artists' % \
            {'base_url': BASE_URL},
            params=params, headers=headers).json()['items']
        for i, a in enumerate(artists):
            # TODO: Come up with something better here
            a['affinity'] = len(artists) * 2 - i
        return artists
