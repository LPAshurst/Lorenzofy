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

model = vosk.Model("./model")
devices_found = sd.query_devices(kind="input")
print(len(devices_found))
pprint.pprint(devices_found)
# args.samplerate = int(device_info['default_samplerate'])


try:
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    print('result')
                    result = json.loads(rec.Result())
                    print(result)
                else:
                    result = json.loads(rec.PartialResult())
                    print('partial')
                    print(result['partial'])
                    for token in result['partial'].upper().split():
                        if token in trigger_to_song:
                            just_now = time.time()
                            if most_recent_play is None or minimum_delta < just_now - most_recent_play:
                                most_recent_play = just_now
                                track = trigger_to_song[token]['track']
                                # FIXME: consider storing whatever was already playing and resuming that after the interruption
                                try:
                                    sp.start_playback(uris=[track['uri']],
                                                    device_id='6fde915182d81765570c865de2361439b180d562',  # FIXME: what to do here??
                                                    position_ms=track['start'])
                                    sleep(s_from_ms(track['stop'] - track['start']))
                                    sp.pause_playback()
                                except:
                                    print("Unexpected error:", sys.exc_info()[0])
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')

    sd.DeviceList()

    # search_query = f'track:{name_query}'
    # #So the limit is only one so its only finding one song rn
    # results = sp.search(q=search_query, type='track', limit=5)

    # # print(json.dumps(results, indent=4))
    # track_uri = results['tracks']['items'][0]['uri']
    # sp.start_playback(device_id=device_id, uris=[track_uri])



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
