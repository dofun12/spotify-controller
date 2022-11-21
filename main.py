# This is a sample Python script.
import pprint
import logging
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
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


def create_playlist(playlistname, tracks, description):
    my_user_id = sp.me()['id']
    sp.user_playlist_create(user=my_user_id, name=playlistname, public=True, collaborative=False, description=description)
    playlist_created = find_playlists(playlistname)
    if playlist_created is None:
        return

    pos = 1
    for track in tracks:
        logger.info(f" Adding track {track['track_id']} of album {track['album_id']}")
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
        'Elvis Presley',
        'The Beatles',
        'Imagine Dragons',
        'Ratt',
        'Morrissey',
        'Bruno Mars',
        'Twisted Sisters',
        'Legião Urbana',
        'Raimundos',
        'Titãs',
        'Capital Inicial',
        'Os Paralamas do Sucesso',
        'Rita Lee',
        'Raul Seixas',
        'System of a Down',
        'Foo Fighters',
        'The Dreadnoughts',
        'Pitty',
        'Racionais MC\'s',
        'Projota',
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
        'Black Sabbath',
        'Dio',
        'U2',
        'Judas Priest',
        'DragonForce',
        'Raimundos',
        'Tarja',
        'The Doors',
        'Pink Floyd',
        'Deep Purple',
        'Ramones',
        'Rush',
        'Rainbow',
        'The Who',
        'Kansas',
        'Bon Jovi',
        'Guns N\' Roses',
        'Duran Duran',
        'Def Leppard',
        'Whitesnake',
        'Boston',
        'Dio',
        'Creedence Clearwater Revival',
        'Eric Clapton',
        'Stratovarius',
        'Megadeath',
        'Metallica'
    ]

    i = 0
    top_ten_artists = []
    while i <= 10:
        artists_len = len(artists)
        winner_pos = random.randrange(0, artists_len - 1)
        winner = artists[winner_pos]
        top_ten_artists.append(winner)
        artists.pop(winner_pos)
        i = i + 1

    artist_discovery = ArtistTracksDicovery(sp)
    db = DBManager()
    selected_tracks = []
    for artist_name in top_ten_artists:
        print(artist_name)
        artist = search(artist_name, 'artist', True)
        artist_discovery.discovery_artist_albums(artist)
        selected_tracks.extend(db.find_tracks_by_artist(artist['id']))

    day_as_string = today.strftime("%Y-%m-%d")
    if len(selected_tracks) == 0:
        exit(0)

    top_ten_artists_string = (' , '.join(top_ten_artists))
    description = f'Today artists: {top_ten_artists_string}'
    create_playlist(f'Generated Playlist {day_as_string}', selected_tracks, description)

    # list_playlists()
    # results = sp.current_user_playlists(limit=20,offset=0)
    # for idx, item in enumerate(results['items']):
#        track = item['track']
#       print(idx, track['artists'][0]['name'], " – ", track['name'])
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
