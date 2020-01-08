import graph
import flask
import pymongo
import json
import networkx as nx
from networkx.readwrite import json_graph
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from flask import Flask, render_template, request
app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

spotipy_client_id = 'king-nith'
spotipy_client_secret = 'palutena-is-trash'
spotipy_redirect_uri = 'pikachu is aids'
username = 'wolf for the win'
scope = None


# token = util.prompt_for_user_token(username, scope, client_id=spotipy_client_id, client_secret=spotipy_client_secret, redirect_uri=spotipy_redirect_uri)
credentials = oauth2.SpotifyClientCredentials(client_id=spotipy_client_id, client_secret=spotipy_client_secret)
token = credentials.get_access_token()

if token:
    spotify = spotipy.Spotify(auth=token)
else:
    print("can't get token for ", username)

G = None
@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        start_song = request.form['startSong']
        end_song = request.form['endSong']
        track_list = graph.getTrackList(start_song, end_song)
        return ', '.join(track_list)
    return render_template('index.html', error = error)
if __name__ == '__main__':
    app.run(debug=True)




