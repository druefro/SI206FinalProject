import requests
import json
import sqlite3
import APIKeys
import spotipy
import spotipy.oauth2 as oauth2
import MusicGrab

conn = sqlite3.connect("spotify.sqlite")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS SpotifyData (rating_spotify INTEGER, song TEXT")
''' Using track_number (rating), name, create a date column of table that just has the day we collected it on,
make separate columns for : rating_spotify, rating_itunes, date, song, rating_score'''

