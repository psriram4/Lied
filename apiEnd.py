import graph
import flask
import pymongo
import json
import networkx as nx
from networkx.readwrite import json_graph
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from flask import Flask, json, g, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

spotipy_client_id = 'd7afc31707824ecabe5583dc87bbfb31'
spotipy_client_secret = 'b19fd0ce632243b4a74ae23516e48db9'
spotipy_redirect_uri = 'http://localhost/'
username = 'amithcskills'
scope = None


# token = util.prompt_for_user_token(username, scope, client_id=spotipy_client_id, client_secret=spotipy_client_secret, redirect_uri=spotipy_redirect_uri)
credentials = oauth2.SpotifyClientCredentials(client_id=spotipy_client_id, client_secret=spotipy_client_secret)
token = credentials.get_access_token()

if token:
    spotify = spotipy.Spotify(auth=token)
    print(token)
else:
    print("can't get token for ", username)

G = None
@app.route('/api', methods=['POST'])
def index():
    error = None
    if request.method == 'POST':
        data = json.loads(request.data)
        # start_song = request.form['startSong']
        # end_song = request.form['endSong']
        start_song = data['startSong']
        end_song = data['endSong']
        track_list = graph.getTrackList(start_song, end_song)
        return ', '.join(track_list)
    return 'f'
    # return render_template('index.html', error = error)
# if __name__ == '__main__':
#     app.run(debug=True)
