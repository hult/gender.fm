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

def lastfm():
    page = 1
    while True:
        r = requests.get('http://ws.audioscrobbler.com/2.0',
            params={
                'method': 'chart.gettopartists',
                'api_key': os.getenv('LASTFM_API_KEY'),
                'format': 'json',
                'limit': 1000,
                'page': page
            }).json()
        for a in r['artists']['artist']:
            yield a
        page += 1

def main():
    for i, artist in enumerate(itertools.chain(echonest(), lastfm())):
        print i
        if artist['name'] in cache:
            continue
        gender, gender_provider = genderfm.get_gender(artist)
        cache[artist['name']] = (gender, gender_provider)

        if i > 0 and i % 100 == 0:
            pickle.dump(cache, open("cache", "w"))

pickle.dump(cache, open("cache", "w"))

if __name__ == '__main__':
    main()
