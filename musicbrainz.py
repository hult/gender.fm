import requests
import urllib
import xmltodict

def gender(artist):
    artistname = artist.encode('utf-8')
    params = { 'query': 'artist:%s' % artistname }
    r = requests.get('http://musicbrainz.org/ws/2/artist',
       params=params)
    if r.status_code == 200:
        data = xmltodict.parse(r.text)
        if 'metadata' in data and 'artist-list' in data['metadata'] \
            and 'artist' in data['metadata']['artist-list']:
            a = data['metadata']['artist-list']['artist']
            if isinstance(a, list):
                a = a[0]
            return a.get('gender')
    return None
