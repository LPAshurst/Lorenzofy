# Lorenzofy

This repo houses my attempt at using the spotify API. As of right now my program only plays music based off my spotify account. Further research into the Spotify would be needed to enable other people to use this application with their respective account. I access my Spotify API key through I will not be including due to privacy reasons. You can get your own private client ID/KEY [here](https://developer.spotify.com/) by loging into spotify or creating an account and following the directions in the dashboard to create your own project. Once you recieve your private cline ID/KEY you can make a .env file that looks like so:


SPOTIPY_CLIENT_ID='********************'

SPOTIPY_CLIENT_SECRET='**********************'

SPOTIPY_REDIRECT_URI='https://google.com/' (This link should be used in your spotify project dashboard)

One useful thing to keep in mind is that the following packages should be installed before using this project:
```
pip install dotenv
pip install sounddevice
pip install spotipy --upgrade
pip install vosk
pip install pyaudio
wget https://alphacephei.com/vosk/models/vosk-model-en-us-aspire-0.2.zip
unzip vosk-model-en-us-aspire-0.2.zip
mv vosk-model-en-us-aspire-0.2 model
python speech_based_play.py
```
So far I have implemented the following:

1) Connecting to Spotify via Spotipy
2) Getting the list of device id's based on my account and prompting the user to select which device they want to play music on
3) Asking the user what song they would like to hear
4) Playing said song on the selected device
