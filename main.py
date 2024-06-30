import requests
import os
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap5
from utils.spotifyAPI import searchSpotify
import sqlite3
from random import randint


app = Flask(__name__)
bootstrap = Bootstrap5(app)

database = sqlite3.connect("database.db", check_same_thread=False)
cursor = database.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS rooms (roomid TEXT PRIMARY KEY, spotify_id TEXT, playlist_name TEXT)")

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        roomid = request.form.get('roomID')
        if len(roomid) != 8:
            return render_template("index.html", response="Invalid room id", comment="A room ID should be composed of number and have a lenght of 8 characters", type="error", roomid=roomid)
        roomSearch = cursor.execute("SELECT * FROM rooms WHERE roomid = ?", (roomid,)).fetchone()
        if roomSearch:
            return render_template("index.html", response="We found your collaborative playlist", comment="It is a great news, click the button below to access it.", type="success", roomid=roomid)
        else:
            return render_template("index.html", response="We could not find your collaborative playlist", comment="Please check the room id and try again or create one.", type="error", roomid=roomid)
    return render_template("index.html")

@app.route('/create', methods=["POST"])
def create_playlist():
    playlistName = request.form.get('roomName')
    if not playlistName:
        return render_template("create.html", response="Invalid playlist name", comment="Please provide a valid playlist name", type="error")
    playlistID = "test"
    # check if the room id already exists
    roomid = randint(10000000, 99999999)
    while cursor.execute("SELECT * FROM rooms WHERE roomid = ?", (roomid,)).fetchone():
        roomid = randint(10000000, 99999999)
    cursor.execute("INSERT INTO rooms (roomid, spotify_id, playlist_name) VALUES (?, ?, ?)", (roomid, playlistID, playlistName))
    database.commit()
    return render_template("create.html", response="Playlist created successfully", comment="Enjoy the night \U0001f57a", type="success", roomid=roomid)

@app.route('/search/<string:roomid>', methods=['GET', 'POST'])
def main_app(roomid):
    if len(roomid) != 8 or not cursor.execute("SELECT * FROM rooms WHERE roomid = ?", (roomid,)).fetchone():
        return main()
    playlistName = cursor.execute("SELECT playlist_name FROM rooms WHERE roomid = ?", (roomid,)).fetchone()[0]
    # handle the POST request
    if request.method == 'POST':
        search = request.form.get('search')
        result = searchSpotify(search)
        return render_template("found.html", query=search, tracks=result, roomid=roomid, playlistName=playlistName)

    # otherwise handle the GET request
    return render_template("search.html", roomid=roomid, playlistName=playlistName)

@app.route('/add/<string:roomid>/<string:trackid>', methods=['GET'])
def add_to_playlist(roomid, trackid):
    print(roomid)
    print(trackid)
    if not os.getenv("n8n_webhook"):
        return render_template("add.html", response="No n8n webhook provided", comment="Please provide a n8n webhook in the .env file", type="error", roomid=roomid)
    try:
        data = requests.get(os.getenv("n8n_webhook") + "/" + roomid + "/" + trackid)
        if data.json()['message'] == 'Workflow was started':
            return render_template("add.html", response="Track added to playlist successfully", comment="Enjoy the night \U0001f57a", type="success", roomid=roomid)

        else:
            return render_template("add.html", response='Invalid response from server', comment=data.text, type="error", roomid=roomid)
    except requests.exceptions.RequestException as e:
        return render_template("add.html", response='Request failed', comment=e, type="error", roomid=roomid)


if __name__ == '__main__':
    if not os.getenv("client_id") or not os.getenv("client_secret") or not os.getenv("n8n_webhook"):
        print("Please provide client_id, client_secret and n8n_webhook in the .env file")
        exit(1)
    if os.getenv("enviroment") != "production":
        app.run(debug=True, port="3000", host="0.0.0.0")
    else:
        app.run(debug=False, port="3000", host="0.0.0.0")