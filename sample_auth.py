import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

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

# sample code

artist_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

results = spotify.artist_albums(artist_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])