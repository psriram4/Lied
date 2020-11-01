# Lied
An app that creates a transition playlist given two songs or artists, transition from one genre to another. Uses the Spotipy API and a graph traversal algorithm to generate the playlist.

Inspired by Boil The Frog. Link: http://boilthefrog.playlistmachinery.com

# Authors
The official public repository for theBridge. Want to contribute? Contact Amith Chivukula (amithc2@illinois.edu) or Pranav Sriram (psriram2@illinois.edu)

# Building Project 
In theBridge folder, run the following command: 

``` FLASK_APP=$PWD/app/http/api/apiEnd.py FLASK_ENV=development python -m flask run --port 4433 ```

Next, in the web_app folder: 

``` npm start ```
