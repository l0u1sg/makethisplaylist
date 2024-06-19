import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def searchSpotify(spotifySearch, limit=1):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")))
    results = sp.search(q=spotifySearch, limit=limit)
    trackName = results['tracks']['items'][0]['name']
    trackArtist = results['tracks']['items'][0]['artists'][0]['name']
    trackAlbum = results['tracks']['items'][0]['album']['name']
    trackPreview = results['tracks']['items'][0]['preview_url']
    trackImage = results['tracks']['items'][0]['album']['images'][0]['url']
    trackID = results['tracks']['items'][0]['uri']
    return (trackName, trackArtist, trackAlbum, trackPreview, trackImage, trackID)
