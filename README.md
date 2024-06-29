# Make This Playlist

Make This Playlist is a web application that allows anyone to add music to a Spotify playlist without needing a Spotify account. The application is accessible at the following address: [Make This Playlist](https://makethisplaylist.louisgallet.fr).

## Features
- Creation of a playlist
- Search for music on Spotify
- Add music to a playlist

## Installation

### Docker
You can install the application via Docker. To do this, execute the following command:
```bash
docker run -d \
  -p 80:3000 \
  -e client_id=SPOTIFY_CLIENT_ID \
  -e client_secret=SPOTIFY_CLIENT_SECRET \
  -e n8n_webhook=N8N_WEBHOOK_URL \
  gitea.louisgallet.fr/lgallet/makethisplaylist:latest
```

### Manually
To install the application manually, clone the repository and install the dependencies:
```bash
git clone https://gitea.louisgallet.fr/lgallet/makethisplaylist.git
cd makethisplaylist
pip install -r requirements.txt
python main.py
```