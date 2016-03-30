import requests
import json
import urllib
from genderize import Genderize

class GenderizeIO(object):
    __name__ = 'genderizeio'

    def __init__(self, api_key=None):
        self._api = Genderize(api_key=api_key)

    def gender(self, artist):
        first_name = artist.split(' ')[0]
        response = self._api.get([first_name])
        if response[0]['gender'] is not None \
            and response[0]['probability'] > 0.75 \
            and response[0]['count'] > 50:
            return response[0]['gender']
        else:
            return None
