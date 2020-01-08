import sys
import networkx as nx
import json
import matplotlib.pyplot as plt
import math
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import pymongo
from networkx.readwrite import json_graph
import web_app

'''
Create an artist similarity graph and run bidirectional dijkstra's
'''

def loadFromDatabase(collection_name, item_id):
    bridge_db = web_app.mongo_client["bridge_db"]
    collection = bridge_db[collection_name]
    document = collection.find_one({ "_id": item_id})
    return document


def createGraph(data_col_name, track_data_col_name):
    web_app.G = nx.Graph()

    data = loadFromDatabase(data_col_name, 1)
    track_data = loadFromDatabase(track_data_col_name, 1)

    try:
        artists = data['artists']
    except data is None:
        status = 'Error in parsing data from path'
    for artist in artists:
        web_app.G.add_node(artist['id'])
        for neighbor in artist['related']:
            if neighbor['id'] not in web_app.G.nodes:
                web_app.G.add_node(neighbor['id'])

            if not web_app.G.has_edge(artist['id'], neighbor['id']):
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


    bridge_db = web_app.mongo_client["bridge_db"]
    graph_col = bridge_db["graph_col"]

    graph_data = json_graph.node_link_data(G)
    graph_json = {}
    graph_json['_id'] = 1
    graph_json['data'] = graph_data

    inserted_graph = graph_col.insert_one(graph_json)
    print(inserted_graph.inserted_id, " - graph data has been inserted")


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
        top_tracks = web_app.spotify.artist_top_tracks(artist, country='US')
        min_distance = 100000000
        next_track = None

        curr_track_features = web_app.spotify.audio_features(curr_track)[0]
        for top_track in top_tracks['tracks']:
            next_track_features = web_app.spotify.audio_features(top_track['id'])[0]
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
    start_artist = web_app.spotify.track(start_song)['artists'][0]['id']
    end_artist = web_app.spotify.track(end_song)['artists'][0]['id']

    status = 'ok'
    try:
        length, path = nx.bidirectional_dijkstra(web_app.G, start_artist, end_artist)
    except:
        status = 'No path between ' + start_song + ' and ' + end_song

    tracks = minimizeTracks(path, start_song, end_song)

    track_names = []
    for track in tracks:
        track_names.append(web_app.spotify.track(track)['name'])

    return track_names


def getTrackList(start_song, end_song):
    data_col_name = "artist_col"
    tracks_col_name = "tracks_col"

    if "graph_col" in web_app.mongo_client["bridge_db"].list_collection_names():
        graph_data = loadFromDatabase("graph_col", 1)
        web_app.G = json_graph.node_link_graph(graph_data['data'])
    else:
        createGraph(data_col_name, tracks_col_name)

    track_list = findShortestPath(start_song, end_song)
    return track_list



