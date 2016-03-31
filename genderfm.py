import musicgraph
import musicbrainz
import spotify
import genderizeio
import cache
import time
import pprint
import sys
import os
import pickle

gender_providers = [
    musicgraph.MusicGraph(os.getenv('MUSICGRAPH_API_KEY')),
    musicbrainz,
    genderizeio.GenderizeIO(os.getenv('GENDERIZEIO_API_KEY')),
]

try:
    cache = pickle.load(open("cache", "r"))
except:
    cache = {}

def add_gender(artists):
    """Given a number of Spotify artists, return them with a gender,
    and the provider of that gender, added.
    """
    for i, artist in enumerate(artists):
        print i
        gender, gender_provider = get_gender_cached(artist)
        artist['gender'] = gender
        artist['gender_provider'] = gender_provider
    return artists

def get_gender(artist):
    """Given an artist (a dictionary with a name property), return
    a tuple with its gender and the name of the provider of that
    gender. If no gender is found, return None, None.
    """
    for provider in gender_providers:
        gender = provider.gender(artist['name'])
        print artist['name'], gender, provider.__name__
        if gender is not None:
            break
    return gender, gender is not None and provider.__name__ or None

def get_gender_cached(artist):
    if artist['name'] in cache:
        print "CACHE HIT", artist['name']
        return cache[artist['name']]
    return get_gender(artist)

def gender_score(gender):
    return {
        'male': 0.0,
        'female': 1.0,
        'both': 0.5
    }.get(gender)

def to_genderfm_artist(artist):
    desired_image_width = 300
    res = {
        "name": artist["name"],
        "gender": artist["gender"],
    }
    images = sorted(artist.get("images", []), key=lambda i: abs(desired_image_width - i["width"]))
    if len(images) > 0:
        res["image_url"] = images[0]["url"]

    return res

def genderfm(access_token):
    spotify_service = spotify.Spotify(access_token)
    artists = spotify_service.top_artists(time_range='long_term')
    artists_with_gender = add_gender(artists)
    total_score = 0.0
    total_affinity = 0
    res = {"artists": [], "score": 0.5}
    for i, artist in enumerate(artists_with_gender):
        score = gender_score(artist['gender'])
        if score is not None:
            total_score += score * int(artist['affinity'])
            total_affinity += int(artist['affinity'])
        print artist['name'], artist['affinity'], artist['gender_provider'], artist['gender']
        res["artists"].append(to_genderfm_artist(artist))
    res["score"] = round((total_score / total_affinity) * 100, 1)
    return res

def main():
    import pprint
    pprint.pprint(genderfm(os.getenv('SPOTIFY_ACCESS_TOKEN')))

if __name__ == '__main__':
    main()
