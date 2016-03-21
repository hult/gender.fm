import requests
import json
import urllib
from genderize import Genderize

def gender(artist):
    first_name = artist.split(' ')[0]
    response = Genderize().get([first_name])
    if response[0]['gender'] is not None \
        and response[0]['probability'] > 0.75 \
        and response[0]['count'] > 50:
        return response[0]['gender']
    else:
        return None
