# This is a sample Python script.
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def list_playlists():
    playlists = sp.current_user_playlists(limit=10, offset=0)
    for idx, playlist in enumerate(playlists['items']):
        # print(playlist)
        print(playlist['id']+" - "+playlist['name'])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    list_playlists()
    # results = sp.current_user_playlists(limit=20,offset=0)
    #for idx, item in enumerate(results['items']):
#        track = item['track']
 #       print(idx, track['artists'][0]['name'], " – ", track['name'])
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
