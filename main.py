import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap5

from spotifySearch import searchSpotify


app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/', methods=['GET', 'POST'])
def main_app():
    # handle the POST request
    if request.method == 'POST':
        search = request.form.get('search')
        result = searchSpotify(search)
        return render_template("found.html", query=search, tracks=result)

    # otherwise handle the GET request
    return render_template("index.html")

@app.route('/add/<string:trackid>', methods=['GET'])
def add_to_playlist(trackid):
    if not os.getenv("n8n_webhook"):
        return 'n8n_webhook not set'
    if not trackid:
        return 'No trackid provided'
    try:
        data = requests.get(os.getenv("n8n_webhook") + "/" + trackid)
        if data.json()['message'] == 'Workflow was started':
            return 'Track added to playlist'
        else:
            return 'Invalid response from server: {}'.format(data.text)
    except requests.exceptions.RequestException as e:
        return 'Request failed: {}'.format(e)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port="3000", host="0.0.0.0")