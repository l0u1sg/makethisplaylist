# Make This Playlist

Make This Playlist is a web application that allows anyone to add music to a Spotify playlist without needing a Spotify account. The application is accessible at the following address: [Make This Playlist](https://makethisplaylist.louisgallet.fr).

## Features
- Creation of a playlist
- Search for music on Spotify
- Add music to a playlist

## Requirements
- n8n account or instance
- n8n workflow (import [n8n workflow file](https://gitea.louisgallet.fr/lgallet/makethisplaylist/src/branch/main/n8n_workflow.json) into your account and set your Spotify credentials)
- Spotify Developer Account

## Installation

### Docker
You can install the application via Docker. To do this, execute the following command:  
For the webhook URLs, make sure to remove the parameters, as they will be added directly by the application.
```bash
docker run -d \
  -p 80:3000 \
  -e client_id=SPOTIFY_CLIENT_ID \
  -e client_secret=SPOTIFY_CLIENT_SECRET \
  -e n8n_webhook_create_playlist=N8N_WEBHOOK_URL \
  -e n8n_webhook_add_tracks=N8N_WEBHOOK_URL \
  -e environment=production \
  -e hostname=https://example.com \
  -v "$(pwd)/database.db:/app/database.db" \
  gitea.louisgallet.fr/lgallet/makethisplaylist:latest
```

### Manually
To install the application manually, clone the repository and install the dependencies:
```bash
git clone https://gitea.louisgallet.fr/lgallet/makethisplaylist.git
cd makethisplaylist
pip install -r requirements.txt
cp .env.example .env
python main.py
```