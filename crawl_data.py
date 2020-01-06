import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json

spotipy_client_id = 'your-client-id'
spotipy_client_secret = 'your-client-secret'
spotipy_redirect_uri = 'your-redirect-uri'
username = 'your-username'
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

        song_data[artist['id']] = getPopularTracks(artist)
        

        crawl_data.append(artist)
        seen_artists.append(artist['id'])


        # constraint, modify the constant below to determine how many artists we store related artists for
        if len(seen_artists) > 20:
            break

    data['artists'] = crawl_data
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    with open('tracks.txt', 'w') as outfile:
        json.dump(song_data, outfile)

    print("length of crawl data: ", len(crawl_data))
    return crawl_data
        

queue = []
    
init_artist = spotify.artist('spotify:artist:4gzpq5DPGxSnKTe4SA8HAU')
artist = {}

artist['name'] = init_artist['name']
artist['popularity'] = init_artist['popularity']
artist['id'] = init_artist['id']

queue.append(artist)

print("queue prepared. crawl starting...")
crawl(queue)
print("crawl done.")


