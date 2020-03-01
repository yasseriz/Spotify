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


spotifySourceUser = '22k55eomuzfcetiuqubev63mq'

# Obtaining details from good playlist
goodPlaylistID = '4opEbIc7A6MEZAytHj510i'
goodPlaylist = sp.user_playlist(spotifySourceUser, goodPlaylistID)
goodTracks = goodPlaylist["tracks"]
goodSongs = goodTracks["items"] 
while goodTracks['next']:
    goodTracks = sp.next(goodTracks)
    for item in goodTracks["items"]:
        goodSongs.append(item)

# print(goodSongs)
goodids = []
for i in range(len(goodSongs)):
    goodids.append(goodSongs[i]['track']['id'])


# Obtaining features at 50 songs at once
goodFeatures = []
for i in range(0, len(goodids), 50):
    audiofeatures = sp.audio_features(goodids[i:i+50])
    for track in audiofeatures:
        goodFeatures.append(track)
        goodFeatures[-1]['target'] = 1

# Obtaining details from bad playlist
badPlaylistID = '1mwPlkOdmpl4fsFN9vsbTx'
badPlaylist = sp.user_playlist(spotifySourceUser, badPlaylistID)
badTracks = badPlaylist['tracks']
badSongs = badTracks['items']

while badTracks['next']:
    badTracks = sp.next(badTracks)
    for item in badTracks["items"]:
        badSongs.append(item)

badids = []
for i in range(len(badSongs)):
    badids.append(badSongs[i]['track']['id'])

print(len(badids))

# Obtaining features at 50 songs at once
badFeatures = []
for i in range(0, len(badids), 50):
    audiofeatures = sp.audio_features(badids[i:i+50])
    for track in audiofeatures:
        badFeatures.append(track)
        badFeatures[-1]['target'] = 1

goodTrainingData = pd.DataFrame(goodFeatures)
badTrainingData = pd.DataFrame(badFeatures)