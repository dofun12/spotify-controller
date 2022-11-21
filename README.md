# About Project
This projects creates a playlist on Spotify using a set of artists.
The main objective, is build a new playlist Daily with random songs of selected artists.

# Set this env variables
## Mongo db Connection Properties
MONGODB_HOST=localhost;
MONGODB_PORT=27017";
MONGODB_PWD=root";
MONGODB_USER=root";

## Spotify Client Properties
SPOTIPY_CLIENT_ID=<your-spotify_client_id>;
SPOTIPY_CLIENT_SECRET=<yout-spotify_client_secret>;
SPOTIPY_REDIRECT_URI=http://localhost:8080

## Good to use on Containers such docker
PYTHONUNBUFFERED=1;

## Get Spotify Info here
https://developer.spotify.com/dashboard/applications


## Usage
python main.py