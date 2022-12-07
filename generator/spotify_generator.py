import logging
from datetime import date
import spotipy
import yaml
from spotipy.oauth2 import SpotifyOAuth
import random
from database.db_manager import DBManager
from discovery.artist_tracks_discovery import ArtistTracksDicovery

logger = logging.getLogger('generator.spotify_generator')
logging.basicConfig(level='INFO')


class SpotifyGenerator:

    def __init__(self):
        self.scope = "user-library-read,playlist-read-private,playlist-modify-private,playlist-modify-public"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.all_tracks = set()

    # Press Shift+F10 to execute it or replace it with your code.
    # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

    def print_hi(self, name):

        # Use a breakpoint in the code line below to debug your script.
        print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    def search(self, query, type, first_result):
        result = self.sp.search(q=query, type=type)
        # pprint.pprint(result)
        items = result['artists']['items']
        if first_result:
            return result['artists']['items'][0]
        return items
        # pprint.pprint(result['artists']['items'][0])
        # print(result['artists']['items'][0]['name'])

    def load_configs(self):
        with open('config.yml', 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def create_playlist(self, playlistname, tracks, description):
        my_user_id = self.sp.me()['id']
        self.sp.user_playlist_create(user=my_user_id,
                                     name=playlistname,
                                     public=True,
                                     collaborative=False,
                                     description=description)
        playlist_created = self.find_playlists(playlistname)

        if playlist_created is None:
            return None

        pos = 1
        for track in tracks:
            logger.info(f" Adding track {track['track_id']} of album {track['album_id']}")
            self.sp.playlist_add_items(playlist_created['id'], [track['track_id']])
            pos = pos + 1
        return playlist_created

    def find_playlists(self, playlist_name):
        playlists = self.sp.current_user_playlists(limit=10, offset=0)
        for idx, playlist in enumerate(playlists['items']):
            # print(playlist)
            if playlist_name == playlist['name']:
                return playlist
            # print(playlist['id'] + " - " + playlist['name'])
        return None

    def list_playlists(self):
        playlists = self.sp.current_user_playlists(limit=10, offset=0)
        for idx, playlist in enumerate(playlists['items']):
            # print(playlist)
            print(playlist['id'] + " - " + playlist['name'])

    # Press the green button in the gutter to run the script.
    def generate(self):
        config = self.load_configs()
        artists = config.get('artists')

        i = 0
        top_ten_artists = []
        while i <= 20:
            artists_len = len(artists)
            winner_pos = random.randrange(0, artists_len - 1)
            winner = artists[winner_pos]
            top_ten_artists.append(winner)
            artists.pop(winner_pos)
            i = i + 1

        artist_discovery = ArtistTracksDicovery(self.sp)
        db = DBManager()
        selected_tracks = []
        for artist_name in top_ten_artists:
            print(artist_name)
            artist = self.search(artist_name, 'artist', True)
            artist_discovery.discovery_artist_albums(artist)
            selected_tracks.extend(db.find_tracks_by_artist(artist['id'], limit=5))
        today = date.today()
        day_as_string = today.strftime("%Y-%m-%d")
        if len(selected_tracks) == 0:
            exit(0)

        top_ten_artists_string = (' , '.join(top_ten_artists))
        description = f'Today artists: {top_ten_artists_string}'
        playlist_name = f'# Generated Playlist {day_as_string}'
        generated_playlist = self.create_playlist(playlist_name, selected_tracks, description)
        if generated_playlist is None:
            return {"success": False, "message": "Playlist not created!"}
        return {"success": True, "created_playlist": generated_playlist, "description": description}
