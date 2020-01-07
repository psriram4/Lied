import sys
import networkx as nx
import json
import matplotlib.pyplot as plt
import math
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import pymongo

'''
Create an artist similarity graph and run bidirectional dijkstra's
'''

client = pymongo.MongoClient("mongodb://localhost:27017/")

spotipy_client_id = 'a8a57761a69c4cadbc21223798fdf799'
spotipy_client_secret = '2882513df3d24e46a89e034dd16ddf4f'
spotipy_redirect_uri = 'http://localhost/'
username = 'pranav.sriram'
scope = None

# token = util.prompt_for_user_token(username, scope, client_id=spotipy_client_id, client_secret=spotipy_client_secret, redirect_uri=spotipy_redirect_uri)
credentials = oauth2.SpotifyClientCredentials(client_id=spotipy_client_id, client_secret=spotipy_client_secret)
token = credentials.get_access_token()

if token:
    spotify = spotipy.Spotify(auth=token)
else:
    print("can't get token for ", username)


G = nx.Graph()

def createGraph(data_col_name, track_data_col_name):
    # loads the JSON object
    def parseJSON(path):
        obj = None
        with open(path, 'r') as jsonData:
            obj = json.load(jsonData)
        return obj
    
    def loadFromDatabase(collection_name, item_id):
        bridge_db = client["bridge_db"]
        collection = bridge_db[collection_name]
        document = collection.find_one({ "_id": item_id})
        return document


    data = loadFromDatabase(data_col_name, 1)
    track_data = loadFromDatabase(track_data_col_name, 1)

    # data = parseJSON(data_path)
    # track_data = parseJSON(track_data_path)

    try:
        artists = data['artists']
    except data is None:
        status = 'Error in parsing data from path'
    for artist in artists:
        G.add_node(artist['id'])
        for neighbor in artist['related']:
            if neighbor['id'] not in G.nodes:
                G.add_node(neighbor['id'])

            if not G.has_edge(artist['id'], neighbor['id']):
                # calculate edge weight

                # this if statement will be taken out, some of the artists aren't in the dict cuz of the constraint
                if neighbor['id'] not in track_data:
                    edgeWeight = abs(neighbor['popularity'] - artist['popularity'])

                else:
                    artist_tracks = track_data[artist['id']]
                    neighbor_tracks = track_data[neighbor['id']]

                    euclidean_distance = 0
                    euclidean_distance += (artist_tracks['danceability'] - neighbor_tracks['danceability'])**2
                    euclidean_distance += (artist_tracks['energy'] - neighbor_tracks['energy'])**2
                    euclidean_distance += ((1/60)*(artist_tracks['loudness'] - neighbor_tracks['loudness']))**2
                    euclidean_distance += (artist_tracks['speechiness'] - neighbor_tracks['speechiness'])**2

                    edgeWeight = math.sqrt(euclidean_distance)*100 + abs(neighbor['popularity'] - artist['popularity'])
                G.add_edge(artist['id'], neighbor['id'], weight = edgeWeight)


def minimizeTracks(artist_path, first_song, last_song):
    
    tracks = []
    for i in range(len(artist_path)):
        if i == 0:
            tracks.append(first_song)
            curr_track = first_song
            continue

        if i == len(artist_path)-1:
            tracks.append(last_song)
            continue

        artist = artist_path[i]
        top_tracks = spotify.artist_top_tracks(artist, country='US')
        min_distance = 100000000
        next_track = None

        curr_track_features = spotify.audio_features(curr_track)[0]
        for top_track in top_tracks['tracks']:
            next_track_features = spotify.audio_features(top_track['id'])[0]
            euclidean_distance = 0
            euclidean_distance += (curr_track_features['danceability'] - next_track_features['danceability'])**2
            euclidean_distance += (curr_track_features['energy'] - next_track_features['energy'])**2
            euclidean_distance += ((1/60)*(curr_track_features['loudness'] - next_track_features['loudness']))**2
            euclidean_distance += (curr_track_features['speechiness'] - next_track_features['speechiness'])**2

            if euclidean_distance < min_distance:
                next_track = top_track['id']
                min_distance = euclidean_distance

        tracks.append(next_track)
        curr_track = next_track

    return tracks


def findShortestPath(start_song, end_song):
    # print("start track")
    start_artist = spotify.track(start_song)['artists'][0]['id']
    end_artist = spotify.track(end_song)['artists'][0]['id']

    status = 'ok'
    try:
        length, path = nx.bidirectional_dijkstra(G, start_artist, end_artist)
    except:
        status = 'No path between ' + start_song + ' and ' + end_song
    return minimizeTracks(path, start_song, end_song)




if __name__ == '__main__':
    # path = 'data.txt'
    # song_path = 'tracks.txt'

    data_col_name = "artist_col"
    tracks_col_name = "tracks_col"
    createGraph(data_col_name, tracks_col_name)
    start_song = '52VJwrmQflskeWoV0OmEEh'
    end_song = '40bynawzslg9U7ACq07fAj'
    track_list = findShortestPath(start_song, end_song)
    
    for track in track_list:
        print(spotify.track(track)['name'])


