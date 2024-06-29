import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def searchSpotify(spotifySearch, limit=10):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")))
    results = sp.search(q=spotifySearch, limit=limit)

    tracks = []
    for i in range(limit):
        trackName = results['tracks']['items'][i]['name']
        trackArtist = results['tracks']['items'][i]['artists'][0]['name']
        trackAlbum = results['tracks']['items'][i]['album']['name']
        trackPreview = results['tracks']['items'][i]['preview_url']
        trackImage = results['tracks']['items'][i]['album']['images'][0]['url']
        trackID = results['tracks']['items'][i]['uri']
        tracks.append([trackName, trackArtist, trackAlbum, trackPreview, trackImage, trackID])
    return tracks
