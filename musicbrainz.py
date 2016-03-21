import requests
import urllib
import xmltodict

BASE_URL = 'http://musicbrainz.org/ws/2/artist'

def gender(artist):
    artistname = artist.encode('utf-8')
    r = requests.get('%(base_url)s/?%(query)s' % \
      {'base_url': BASE_URL,
       'query': urllib.urlencode(
        {'query': 'artist:%s' % artistname})})
    if r.status_code == 200:
        data = xmltodict.parse(r.text)
        if 'metadata' in data and 'artist-list' in data['metadata'] \
            and 'artist' in data['metadata']['artist-list']:
            a = data['metadata']['artist-list']['artist']
            if isinstance(a, list):
                a = a[0]
            return a.get('gender')
    return None
