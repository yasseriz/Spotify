import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

import pandas as pd 
import requests 


clientID = '4d67ee2b30bf4dbab47486bd630f72fa'
clientSecret = '67e240ad443d4fe6b80dcd0f436a9ca9'
username = 'Yasser Zaheer'
redirectURL = 'http://localhost:7777/callback'

clientCredentialsManager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)

scope = 'user-library-read playlist-read-private'
token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURL)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)