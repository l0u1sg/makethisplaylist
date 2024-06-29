from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap5

from spotifySearch import searchSpotify


app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        search = request.form.get('search')
        result = searchSpotify(search)
        return render_template("found.html", query=search, tracks=result)

    # otherwise handle the GET request
    return render_template("index.html")

@app.route('/test')
def test():
    return render_template("test.html")


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port="3000", host="0.0.0.0")