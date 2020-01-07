import graph
import flask
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        startSong = request.form['startSong']
        endSong = request.form['endSong']
        data_col_name = "artist_col"
        tracks_col_name = "tracks_col"
        graph.createGraph(data_col_name, tracks_col_name)
        status,track_list = graph.findShortestPath(startSong, endSong)
        playList = graph.cleanPathOutput(track_list)
        return ''.join(playList)
    return render_template('index.html', error = error)
if __name__ == '__main__':
    app.run(debug=True)
