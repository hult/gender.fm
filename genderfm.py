import musicgraph
import lastfm
import musicbrainz
import genderizeio
import time
import pprint
import sys
import os

lastfm_service = lastfm.LastFm(os.getenv('LASTFM_API_KEY'))

gender_providers = [
    musicgraph.MusicGraph(os.getenv('MUSICGRAPH_API_KEY')),
    musicbrainz,
    genderizeio,
]

def top_artists_with_gender(username):
    """Given a last.fm username, return a list of last.fm artist objects
    with a gender added. Gender is taken from the first of
    gender_providers that return a non-None response.
    """
    res = []
    for i, artist in enumerate(lastfm_service.top_artists(username)):
        print i
        for provider in gender_providers:
            gender = provider.gender(artist['name'])
            if gender is not None:
                break
        artist['gender'] = gender
        artist['gender_provider'] = gender is not None and provider.__name__ or None
        res.append(artist)
        time.sleep(1.5)
    return res

def gender_score(gender):
    return {
        'male': 0.0,
        'female': 1.0,
        'both': 0.5
    }.get(gender)

def main():
    artists = top_artists_with_gender(sys.argv[1])
    total_score = 0.0
    total_affinity = 0
    for i, artist in enumerate(artists):
        score = gender_score(artist['gender'])
        if score is not None:
            total_score += score * int(artist['affinity'])
            total_affinity += int(artist['affinity'])
        print artist['name'], artist['affinity'], artist['gender_provider'], artist['gender']
    print total_score / total_affinity

if __name__ == '__main__':
    main()
