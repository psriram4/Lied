import sys
import networkx as nx
import json
import matplotlib.pyplot as plt
import math

'''
Node = artist
Edge = .5*artistPop + .5*(energy + instrumentalness + loudness + danceability diff)
'''
def createGraph(data_path, track_data_path):
    # loads the JSON object
    def parseJSON(path):
        obj = None
        with open(path, 'r') as jsonData:
            obj = json.load(jsonData)
        return obj

    # creates graph
    G = nx.Graph()
    data = parseJSON(data_path)
    track_data = parseJSON(track_data_path)
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
                    euclidean_distance += (artist_tracks['loudness'] - neighbor_tracks['loudness'])**2
                    euclidean_distance += (artist_tracks['speechiness'] - neighbor_tracks['speechiness'])**2

                    edgeWeight = math.sqrt(euclidean_distance)*10 + abs(neighbor['popularity'] - artist['popularity'])
                G.add_edge(artist['id'], neighbor['id'], weight = edgeWeight)
    return G


    # BFS to traverse adj list and construct graph
    # if len(artists) > 0:
    #     qBFS = []
    #     qBFS.append(artists[0])
    #     visited.add(artists[0]['name'])
    #     G.add_node(v['name'])
    #     visited = set()
    #     while qBFS:
    #         v = qBFS.pop(0)
    #         for w in v['related']:
    #             if w not in visited:
    #                 G.add_node(w['name'])




if __name__ == '__main__':
  path = 'data.txt'
  song_path = 'tracks.txt'
  graph = createGraph(path, song_path)
  print(graph.nodes)
  # JSON Parsing TEST
  # data = parseJSON(path)
  # print(data['artists'][0]['id'])