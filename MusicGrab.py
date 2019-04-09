#DruErin SI 206 Final Project

import requests
import json
import sqlite3
import APIKeys

## API Keys
client_id = APIKeys.client_id
client_secret = APIKeys.client_secret 

# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way
url = 'https://api.spotify.com'
params = {}
