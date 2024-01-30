#!/usr/bin/env python3
import spotipy
import os
import sys
import webbrowser
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
from json.decoder import JSONDecodeError
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import pprint
import sounddevice as sd
import vosk

scope = "user-read-playback-state,user-modify-playback-state"
load_dotenv()

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

# this next line all you really need to do is press accept and then copy the whole google link in
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

devices = sp.devices()
id_list = []
for index, thing in enumerate(devices['devices']):
    print(f"Device Number: {index + 1}\nDevice name: {thing['name']}, Device Type: {thing['type']}")
    id_list.append(thing['id'])

which_id = int(input("\nPlease enter the device number you would like to play music on: "))

device_id = id_list[which_id - 1]

name_query = input("Enter the name of the song you would like to hear: ") 


search_query = f'track:{name_query}'
#So the limit is only one so its only finding one song rn
results = sp.search(q=search_query, type='track', limit=5)

# print(json.dumps(results, indent=4))
track_uri = results['tracks']['items'][0]['uri']
sp.start_playback(device_id=device_id, uris=[track_uri])



# # Print the first track found
# if len(results['tracks']['items']) > 0:
#     track = results['tracks']['items'][0]
#     print(f"Track Name: {track['name']}")
#     print(f"Artist: {track['artists'][0]['name']}")
#     print(f"Album: {track['album']['name']}")
# else:
#     print(f"No results found for '{track_name}'")
# # playlist_id = 'spotify:album:69MkRYEzxiZ84QmgmPJqdY'
# # results = sp.album(playlist_id)
# # print(json.dumps(results, indent=4))
