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
        self.today = date.today()

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
            return

        pos = 1
        for track in tracks:
            logger.info(f" Adding track {track['track_id']} of album {track['album_id']}")
            self.sp.playlist_add_items(playlist_created['id'], [track['track_id']])
            pos = pos + 1

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
        artists = [
            # 'The Clash',
            'The Offspring',
            'Pearl Jam',
            'Roxette',
            # 'Elvis Presley',
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
            'Jimi Hendrix',
            'Jim Morrison',
            'Skid row',
            'Snow Patrol',
            'Alice in chains',
            'Rhapsody Of Fire',
            'Detonautas Roque Clube',
            'Avenged Sevenfold',
            'Papa Roach',
            'Nat King Cole',
            'Supercombo',
            'Paramore',
            'Racionais MC\'s',
            'Projota',
            'Linkin Park',
            'Audio Slave',
            'Van Halen',
            'KISS',
            'Triumph',
            'Unisonic',
            'Slash',
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
            'Roupa Nova',
            'Johny Cash',
            'Heart',
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
            'Metallica',
            'Alok',
            'Jon Bon Jovi',
            'Engenheiros do Hawaii'
            'Scorpions',
            'Desireless',
            'Otep',
            'Alestorm',
            'Amaranthe',
            'Leaves\' Eyes',
            'Blind Guardian',
            'Ira!',
            'Cássia Eller',
            'Elton John',
            'The Hives',
            'Fleetwood Mac',
            'Hammer Fall',
            'Sex Pistols',
            'Cigarettes After Sex',
            'Eagles',
            'O Rappa',
            'Arctic Monkeys',
            'Greta Van Fleet',
            'The Killers',
            'Stone Sour',
            'Soundgarden',
            'Accept',
            'Angra',
            'Santana',
            'Motörhead',
            'Turisas',
            'Anthrax',
            'Freedom Call',
            'Korpiklaani',
            'Powerwolf',
            'Dark Moor',
            'Avantasia',
            'Iggy Pop',
            'Bruce Springsteen',
            'Alice Cooper',
            'Edguy',
            'The Weeknd',
            'Journey',
            'Frank Sinatra',
            'Slipknot',
            'Five Finger Death Punch',
            'Myrath',
            'Elvenking',
            'Rammstein',
            'KSHMR',
            'KVSH',
            'Avicii',
            'Sia',
            'David Guetta',
            'Rob Zombie',
            'Powerglove',
            'Gotthard',
            'Sonata Arctica',
            'Delain',
            'Alter Bridge',
            'Poison',
            'Jefferson Airplane',
            'Europe',
            'Oasis',
            'Nazareth',
            'Tove Lo',
            'Bee Gees',
            'Zeca Baleiro',
            'Bob Dylan',
            'Korn',
            'Os Paralamas do Sucesso',
            'Epica',
            'FLOW',
            'Justin Timberlake',
            'Ultraje a Rigor',
            'REO Speedwagon',
            'Dream Theater',
            'The Beach Boys',
            'ABBA',
            'a-ha',
            'Édith Piaf',
            'Studio Killers',
            'Johnny Rivers',
            'BABYMETAL',
            'ANIMETAL',
            'Slayer',
            'Genesis',
            'Sepultura',
            'Sabaton',
            'Blue Öyster Cult',
            'Nickelback',
            'Tihuana',
            'Pedra Leticia',
            'Matanza',
            'Red Hot Chili Peppers',
            'The Cure',
            'AC/DC',
            'Within Temptation',
            'Pantera',
            'Foster the People',
            'Volbeat'
        ]

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

        day_as_string = self.today.strftime("%Y-%m-%d")
        if len(selected_tracks) == 0:
            exit(0)

        top_ten_artists_string = (' , '.join(top_ten_artists))
        description = f'Today artists: {top_ten_artists_string}'
        self.create_playlist(f'Generated Playlist {day_as_string}', selected_tracks, description)

        # list_playlists()
        # results = sp.current_user_playlists(limit=20,offset=0)
        # for idx, item in enumerate(results['items']):
    #        track = item['track']
    #       print(idx, track['artists'][0]['name'], " – ", track['name'])
    #    print_hi('PyCharm')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
