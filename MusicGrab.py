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

url = 'https://www.billboard.com/charts/hot-100'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

def generate_token():
    '''Generates token for Spotify API using the API keys'''
    credentials = oauth2.SpotifyClientCredentials(client_id= client_id_, client_secret= client_secret_)
    token = credentials.get_access_token()
    return token
def grab_spotify_data(user = "spotifycharts", playlist_id = "37i9dQZEVXbLRQDuF5jeBp"):
    '''Makes call to Spotify API and returns US Top 50 songs'''
    token = generate_token()
    spotify = spotipy.Spotify(auth = token)
    results = spotify.user_playlist_tracks(user, playlist_id) #large amount of data from top 50 list
    return results
def grab_billboard_data():
    '''Scrapes the Billboard Hot 100 Chart website using BeautifulSoup and returns list of top 100 songs'''
    outer_tag = soup.find("div", class_ = "chart-details ")
    song_tag_list = outer_tag.find_all("div", class_ = "chart-list-item")
    song_list = []
    for song in song_tag_list:
        song_list.append(song["data-title"])
    return song_list

date = str(datetime.datetime.now()).split()[0]

spotify_results = grab_spotify_data()


# song_list = grab_billboard_data()


conn = sqlite3.connect("spotify.sqlite")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS SpotifySongData (song_title TEXT UNIQUE, rating INTEGER, date STRING)")

cur.execute("CREATE TABLE IF NOT EXISTS BillboardData (rating_billboard INTEGER, song TEXT UNIQUE)")

cur.execute("CREATE TABLE IF NOT EXISTS TopSpotifyData (rating INTEGER, song_title TEXT UNIQUE)")

count1 = 0
for song in spotify_results["items"]:
    if count1 == 20:
        break
    song_title = song["track"]["name"]
    rating = spotify_results["items"].index(song) + 1
    sql = "INSERT OR IGNORE INTO SpotifySongData (song_title, rating, date) VALUES (?,?,?)"
    val = (song_title, rating, date)
    rows_modified = cur.execute(sql, val).rowcount
    if rows_modified != 0:
        count1 += 1
conn.commit()

# for song in spotify_results["items"]:
#     song_title = song["track"]["name"]
#     rating = spotify_results["items"].index(song) + 1
#     sql = "INSERT OR IGNORE INTO TopSpotifyData (rating, song_title) VALUES (?,?)"
#     val = (rating, song_title)
#     cur.execute(sql, val)
# conn.commit()

# count = 0
# for song in song_list:
#     if count == 20:
#         break
#     rating_billboard = song_list.index(song) + 1
#     sql = "INSERT OR IGNORE INTO BillboardData (rating_billboard, song) VALUES (?,?)"
#     val = (rating_billboard, song) 
#     rows_modified = cur.execute(sql, val).rowcount
#     if rows_modified != 0:
#         count += 1
# conn.commit()
