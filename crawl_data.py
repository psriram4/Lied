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


def crawl(queue):

    data = {}
    seen_artists = []
    crawl_data = []

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

            if artist['name'] not in seen_artists:
                queue.append(artist_json)

        artist = {}
        artist['name'] = curr_artist['name']
        artist['related'] = related
        crawl_data.append(artist)
        seen_artists.append(curr_artist['name'])


        # constraint, modify the constant below to determine how many artists we store related artists for
        if len(seen_artists) > 200:
            break

    data['artists'] = crawl_data
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

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


