import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap5
from spotifySearch import searchSpotify

import sqlite3


app = Flask(__name__)
bootstrap = Bootstrap5(app)

database = sqlite3.connect("database.db")

@app.route("/", methods=['GET'])
def main():
    return "Hello, World!"

@app.route('/search/<string:roomid>', methods=['GET', 'POST'])
def main_app(roomid):
    # handle the POST request
    if request.method == 'POST':
        search = request.form.get('search')
        result = searchSpotify(search)
        return render_template("found.html", query=search, tracks=result, roomid=roomid)

    # otherwise handle the GET request
    return render_template("index.html")

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
    app.run(debug=True, port="3000", host="0.0.0.0")