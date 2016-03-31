gender.fm
=========

Figure out the gender of your favorite artists.

## Installation ##

### Using virtualenv ###

This step is optional.

    $ virtualenv venv
    $ source venv/bin/activate

### Installing dependencies ###

    $ pip install -r requirements.txt

## Command-line usage ##

    $ python genderfm.py
    0.53242

## Pre-warm the artist gender cache ##

    $ python warm_cache.py

## Start the server ##

    $ python server.py

Then point your browser to `http://localhost:5000/` and log in using
your Spotify account.
