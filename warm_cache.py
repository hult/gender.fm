import pyen
import genderfm
import time
import pickle

en = pyen.Pyen()

try:
    cache = pickle.load(open("cache", "r"))
except:
    cache = {}

results = en.get('artist/top_hottt', results=1000)
for i, artist in enumerate(results['artists']):
    print i
    if artist['name'] in cache:
        continue
    gender, gender_provider = genderfm.get_gender(artist)
    cache[artist['name']] = (gender, gender_provider)

    if i > 0 and i % 100 == 0:
        pickle.dump(cache, open("cache", "w"))

pickle.dump(cache, open("cache", "w"))
