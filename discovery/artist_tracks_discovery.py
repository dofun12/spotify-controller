import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from database.db_manager import DBManager

logger = logging.getLogger('discovery.artist_tracks_discovery')
logging.basicConfig(level='INFO')


class ArtistTracksDicovery:
    all_track = set()

    def __init__(self, sp: spotipy.Spotify):
        self.sp: spotipy.Spotify = sp
        self.db = DBManager()

    def discovery_album_tracks(self, artist, album):
        tracks = []
        results = self.sp.album_tracks(album['id'])
        tracks.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        for i, track in enumerate(tracks):
            self.db.add_track(artist['id'], album['id'], track['id'])
            logger.info('%s. %s', i + 1, track['name'])

    def discovery_artist_albums(self, artist):
        albums = []
        if self.db.find_artist(artist) is not None:
            return

        self.db.add_artist(artist)
        results = self.sp.artist_albums(artist['id'], album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        logger.info('Total albums: %s', len(albums))
        unique = set()  # skip duplicate albums
        for album in albums:
            self.db.add_album(album)
            name = album['name'].lower()
            if name not in unique:
                logger.info('ALBUM: %s', name)
                unique.add(name)
                self.discovery_album_tracks(artist, album)
