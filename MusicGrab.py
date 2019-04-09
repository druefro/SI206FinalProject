#DruErin SI 206 Final Project

import requests
import json
import sqlite3
import APIKeys
import spotipy
import spotipy.oauth2 as oauth2

## API Keys
client_id_ = APIKeys.client_id
client_secret_ = APIKeys.client_secret

def generate_token():
    credentials = oauth2.SpotifyClientCredentials(client_id= client_id_, client_secret= client_secret_)
    token = credentials.get_access_token()
    return token

# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

token = generate_token()
spotify = spotipy.Spotify(auth = token)
results = spotify.user_playlist_tracks(user="spotifycharts", playlist_id="37i9dQZEVXbLRQDuF5jeBp") #large anount of data from top 50 list
print(results['items'][0])
    
conn = sqlite3