from generator.spotify_generator import SpotifyGenerator

if __name__== "__main__":
  spotify_gen = SpotifyGenerator()
  config = spotify_gen.load_configs()
  print(config)