#DruErin SI 206 Final Project

import requests
import json
import sqlite3
import APIKeys
import spotipy
import spotipy.oauth2 as oauth2
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import urllib.request, urllib.parse, urllib.error
import datetime

## API Keys
client_id_ = APIKeys.client_id
client_secret_ = APIKeys.client_secret

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def generate_token():
    credentials = oauth2.SpotifyClientCredentials(client_id= client_id_, client_secret= client_secret_)
    token = credentials.get_access_token()
    return token

# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

# token = generate_token()
# spotify = spotipy.Spotify(auth = token)
# spotify_results = spotify.user_playlist_tracks(user="spotifycharts", playlist_id="37i9dQZEVXbLRQDuF5jeBp") #large anount of data from top 50 list
# print(spotify_results['items'][0])

url = 'https://www.billboard.com/charts/hot-100'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

outer_tag = soup.find("div", class_ = "chart-details ")
song_tag_list = outer_tag.find_all("div", class_ = "chart-list-item")
song_list = []
for song in song_tag_list:
    song_list.append(song["data-title"])
print(song_list)


conn = sqlite3.connect("spotify.sqlite")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS SpotifyData (rating_spotify INTEGER, song_title TEXT, date TEXT")
''' Using track_number (rating), name, create a date column of table that just has the day we collected it on,
make separate columns for : rating_spotify, rating_itunes, date, song, rating_score'''

cur.execute("CREATE TABLE IF NOT EXISTS BillboardData (rating_billboard INTEGER, song TEXT")

date = str(datetime.datetime.now()).split()[0]

for song in song_list:
    rating_billboard = song_list.index(song) + 1
    sql = "INSERT INTO BillboardData (rating_billboard, song) VALUES (?,?)"
    val = (rating_billboard, song) 
    cur.execute(sql, val)
conn.commit()
