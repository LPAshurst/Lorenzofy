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
import queue
import time
import threading

trigger_word = 'fortnight'
play = 'play'
different_bys = ["bye", "by", "buy"]
finding_song = False

q = queue.Queue()
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

model = vosk.Model("./model")
devices_found = sd.query_devices(kind="input")
print(len(devices_found))
pprint.pprint(devices_found)
# args.samplerate = int(device_info['default_samplerate'])


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def play_song(full_sentence):
    finding_song = True
    #These first two checks seem kind of dumb but its to make sure we are using the right keywords to play songs
                
    found_index = None

    if (len(full_sentence) >= 2) and (full_sentence[0] == trigger_word and full_sentence[1] == play):
        print("Im getting here xD")
        for index, string in enumerate(full_sentence):
            for by in different_bys:
                if by in string:
                    found_index = index
                    break
                
        if found_index == None:
            name_query = full_sentence[2:]
            print(name_query)
            #plays just song but no artist

            search_query = f'track:{name_query}'
            #So the limit is only one so its only finding one song rn
            results = sp.search(q=search_query, type='track', limit=5)

            # print(json.dumps(results, indent=4))
            track_uri = results['tracks']['items'][0]['uri']
            sp.start_playback(device_id=device_id, uris=[track_uri])
            finding_song = False
        else:
            name_query = full_sentence[2:found_index]
            artist = full_sentence[found_index + 1:]
            search_query = f'artist:{artist} track:{name_query}'
            results = sp.search(q=search_query, type='track', limit=5)
            track_uri = results['tracks']['items'][0]['uri']
            sp.start_playback(device_id=device_id, uris=[track_uri])
          

try:
    stream = sd.RawInputStream(samplerate=44100, blocksize=8000, device=1, dtype='int16',
                           channels=1, callback=callback)
    with stream:
        print('#' * 80)
        print('Press Ctrl+C to stop the recording')
        print('#' * 80)
    
        rec = vosk.KaldiRecognizer(model, 44100)
        while True:
            data = q.get()

            #I dont like this implementation. Maybe introduce threading?
            if rec.AcceptWaveform(data):
                # This is just a dictionary that stores all the words in one "sentence". Im guessing there is 
                # some leinency to how long a pause can be between sentences but I can figure that out later
                result = json.loads(rec.Result())
                print(result)
                full_sentence = result['text'].split(' ')
                play_song(full_sentence=full_sentence)
                time.sleep(1)
            else:
                continue
            #     #This is the extra shit thats getting printed
            #     result = json.loads(rec.PartialResult())
            #     print('partial')
            #     print(result['partial'])
            #     # for token in result['partial'].upper().split():
            #     #     track = trigger_to_song[token]['track']
            #     #         # FIXME: consider storing whatever was already playing and resuming that after the interruption
            #     #         #Need to add the actual code to start playing shit in this if statement

except KeyboardInterrupt:
    print('\nDone')