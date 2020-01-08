import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json
import pymongo

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

# get related artists

def getMostPopular(arr):
    most_popular_artist = None
    max_popularity = 0
    if len(arr) == 0:
        return None
    else:
        for i in range(len(arr)):
            artist = arr[i]
            if artist['popularity'] > max_popularity:
                most_popular_artist = i
                max_popularity = artist['popularity']
        
    return i


def getPopularTracks(artist):
    artist_id = artist['id']
    top_tracks = spotify.artist_top_tracks(artist_id, country='US')

    popular_tracks = []

    for top_track in top_tracks['tracks']:
        track = {}
        track_features = {}
        track['name'] = top_track['name']
        track['id'] = top_track['id']

        audio_features_json = spotify.audio_features(track['id'])
        audio_features = audio_features_json[0]
        track_features['danceability'] = audio_features['danceability']
        track_features['energy'] = audio_features['energy']
        track_features['loudness'] = audio_features['loudness']
        track_features['speechiness'] = audio_features['speechiness']

        track['features'] = track_features
        popular_tracks.append(track)
    
    return popular_tracks

def getAverageRatings(artist):
    artist_id = artist['id']
    top_tracks = spotify.artist_top_tracks(artist_id, country='US')

    danceability = 0
    energy = 0
    loudness = 0
    speechiness = 0

    for top_track in top_tracks['tracks']:
        audio_features_json = spotify.audio_features(top_track['id'])
        audio_features = audio_features_json[0]
        danceability += audio_features['danceability']
        energy += audio_features['energy']
        loudness += audio_features['loudness']
        speechiness += audio_features['speechiness']

    danceability = danceability / 10
    energy = energy / 10
    loudness = loudness / 10
    speechiness = speechiness / 10

    average_ratings = {}
    average_ratings['danceability'] = danceability
    average_ratings['energy'] = energy
    average_ratings['loudness'] = loudness
    average_ratings['speechiness'] = speechiness

    return average_ratings


def crawl(queue):

    data = {}
    seen_artists = []
    crawl_data = []

    song_data = {}

    while len(queue) != 0:
        idx = getMostPopular(queue)
        curr_artist = queue.pop(idx)
        related_artists = spotify.artist_related_artists(curr_artist['id'])
        related = []

        for artist in related_artists['artists']:
            artist_json = {}
            artist_json['name'] = artist['name']
            artist_json['popularity'] = artist['popularity']
            artist_json['id'] = artist['id']
            related.append(artist_json)

            if artist['id'] not in seen_artists:
                queue.append(artist_json)

        artist = {}
        artist['name'] = curr_artist['name']
        artist['id'] = curr_artist['id']
        artist['popularity'] = curr_artist['popularity']
        artist['related'] = related

        song_data[artist['id']] = getAverageRatings(artist)

        crawl_data.append(artist)
        seen_artists.append(artist['id'])


        # constraint, modify the constant below to determine how many artists we store related artists for
        if len(seen_artists) > 20:
            break

    data['artists'] = crawl_data
    
    # this saves the data to text files, can be removed once database is created
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    with open('tracks.txt', 'w') as outfile:
        json.dump(song_data, outfile)


    # database
    data['_id'] = 1
    song_data['_id'] = 1

    bridge_db = client["bridge_db"]
    artist_col = bridge_db["artist_col"]
    tracks_col = bridge_db["tracks_col"]

    inserted_data = artist_col.insert_one(data)
    inserted_song_data = tracks_col.insert_one(song_data) 

    print(inserted_data.inserted_id, " - data has been inserted")
    print(inserted_song_data.inserted_id, " - song data has been inserted")


    print("length of crawl data: ", len(crawl_data))
    return crawl_data
        

queue = []
    
init_artist = spotify.artist('spotify:artist:4gzpq5DPGxSnKTe4SA8HAU')
artist = {}

artist['name'] = init_artist['name']
artist['popularity'] = init_artist['popularity']
artist['id'] = init_artist['id']

queue.append(artist)


if "bridge_db" in client.list_database_names():
    print("database already exists!")

else: 
    print("queue prepared. crawl starting...")
    crawl(queue)


print("crawl done.")


