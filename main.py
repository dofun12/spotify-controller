# This is a sample Python script.
import pprint
import logging
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from database.db_manager import DBManager
from discovery.artist_tracks_discovery import ArtistTracksDicovery

scope = "user-library-read,playlist-read-private,playlist-modify-private,playlist-modify-public"
logger = logging.getLogger('examples.artist_discography')
logging.basicConfig(level='INFO')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

all_tracks = set()
today = date.today()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def search(query, type, first_result):
    result = sp.search(q=query, type=type)
    # pprint.pprint(result)
    items = result['artists']['items']
    if first_result:
        return result['artists']['items'][0]
    return items
    # pprint.pprint(result['artists']['items'][0])
    # print(result['artists']['items'][0]['name'])


def create_playlist(playlistname, tracks):
    my_user_id = sp.me()['id']
    sp.user_playlist_create(user=my_user_id, name=playlistname, public=True, collaborative=False)
    playlist_created = find_playlists(playlistname)
    if playlist_created is None:
        return

    pos = 1
    for track in tracks:
        sp.playlist_add_items(playlist_created['id'], [track['track_id']])
        pos = pos + 1


def find_playlists(playlist_name):
    playlists = sp.current_user_playlists(limit=10, offset=0)
    for idx, playlist in enumerate(playlists['items']):
        # print(playlist)
        if playlist_name == playlist['name']:
            return playlist
        # print(playlist['id'] + " - " + playlist['name'])
    return None


def list_playlists():
    playlists = sp.current_user_playlists(limit=10, offset=0)
    for idx, playlist in enumerate(playlists['items']):
        # print(playlist)
        print(playlist['id'] + " - " + playlist['name'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    artists = [
        'The Clash',
        'The Offspring',
        'Pearl Jam',
        'Roxette',
        'System of a Down',
        'Foo Fighters',
        'Linkin Park',
        'Audio Slave',
        'Van Halen',
        'KISS',
        'Aerosmith',
        'Iron Maiden',
        'Charlie Brown Jr.',
        'Nightwish',
        'Helloween',
        'Chris Isaak',
        'Coldplay',
        'Eluveitie',
        'Ozzy Osborn',
        'Led Zeppelin',
        'Queen',
        'DragonForce',
        'Raimundos',
        'Tarja',
        'Stratovarius',
        'Megadeath',
        'Metallica'
    ]
    artist_discovery = ArtistTracksDicovery(sp)
    db = DBManager()
    selected_tracks = []
    for artist_name in artists:
        artist = search(artist_name, 'artist', True)
        artist_discovery.discovery_artist_albums(artist)
        selected_tracks.extend(db.find_tracks_by_artist(artist['id']))

    day_as_string = today.strftime("%Y-%m-%d")
    create_playlist(f'Generated Playlist {day_as_string}', selected_tracks)

    # list_playlists()
    # results = sp.current_user_playlists(limit=20,offset=0)
    # for idx, item in enumerate(results['items']):
#        track = item['track']
#       print(idx, track['artists'][0]['name'], " – ", track['name'])
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
