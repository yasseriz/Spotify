import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd 
import requests 


clientID = '4d67ee2b30bf4dbab47486bd630f72fa'
clientSecret = '67e240ad443d4fe6b80dcd0f436a9ca9'

clientCredentialsManager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)

username = 'Yasser Zaheer'
redirectURL = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'

token = util.prompt_for_user_token(username=username, 
                                   scope=scope,
                                   client_id=clientID,
                                   client_secret=clientSecret,
                                   redirect_uri=redirectURL)


def getID(trackName, token, artist):
    headers = { 'Accept':'application/json',
                'Content-Type':'application/json',
                'Authorization':f'Bearer '+token,
    }
    params = [('q', trackName),('type', 'track'),]

    if artist:
        params.append(('artist', artist))
    try:
        response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params, timeout=5)
        responseJson = response.json()
        # print(responseJson)
        firstResult = responseJson['tracks']['items'][0]
        trackID = firstResult['id']
        return trackID
    except:
        return None
    
lucy_id = getID('Lucy', token, artist='The Beatles')
# print(lucy_id)

def getFeatures(trackID, token):
    sp = spotipy.Spotify(auth=token)
    try:
        features =  sp.audio_features([trackID])
        return features[0]

    except:
        return None

lucy_features = getFeatures(lucy_id, token)
# print(lucy_features)

def getRecentlyPlayedTracks(token): 
    headers = { 'Accept':'application/json',
                'Content-Type':'application/json',
                'Authorization':f'Bearer '+token,
    }

    path = 'https://api.spotify.com/v1/' # me/player/recently-played'
    response = requests.get(path+'me'+'/player/recently-played', headers=headers)
    responseJson = response.json()
    print(responseJson)

# getRecentlyPlayedTracks(token)

