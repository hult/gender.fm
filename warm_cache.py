import pyen
import genderfm
import time
import pickle
import requests
import itertools
import os

en = pyen.Pyen()

try:
    cache = pickle.load(open("cache", "r"))
except:
    cache = {}

def echonest():
    return en.get('artist/top_hottt', results=1000)['artists']

def lastfm(country=None):
    page = 1
    params = {
        'method': 'chart.gettopartists',
        'api_key': os.getenv('LASTFM_API_KEY'),
        'format': 'json',
        'limit': 1000,
        'page': page
    }
    artists_key = 'artists'

    if country is not None:
        params['method'] = 'geo.gettopartists'
        params['country'] = country
        artists_key = 'topartists'

    while True:
        r = requests.get('http://ws.audioscrobbler.com/2.0',
            params=params).json()
        for a in r[artists_key]['artist']:
            yield a
        page += 1

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = itertools.cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))

def main():
    for i, artist in enumerate(roundrobin(echonest(), lastfm(), lastfm('Sweden'))):
        print i, artist['name']
        if artist['name'] in cache:
            continue
        gender, gender_provider = genderfm.get_gender(artist)
        cache[artist['name']] = (gender, gender_provider)

        if i > 0 and i % 100 == 0:
            pickle.dump(cache, open("cache", "w"))

if __name__ == '__main__':
    main()
