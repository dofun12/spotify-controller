import spotipy
from fastapi import APIRouter
from spotipy import SpotifyOAuth
from starlette.responses import RedirectResponse

from generator.spotify_generator import SpotifyGenerator

router = APIRouter()

CONTEXT = "/generator"
scope = "user-read-private,user-library-read,playlist-read-private,playlist-modify-private,playlist-modify-public"


@router.get(f"{CONTEXT}/")
async def generate():
    return {"message": "Hello World"}


@router.get(f"{CONTEXT}/login")
async def login():
    auth = SpotifyOAuth(scope=scope)
    print(auth.get_authorize_url())
    return RedirectResponse(auth.get_authorize_url())


@router.get(f"{CONTEXT}/callback")
async def callback(code: str = ""):
    auth = SpotifyOAuth(scope=scope)
    auth.get_access_token(code=code)
    sp = spotipy.Spotify(auth_manager=auth)
    return {"message": "Logado com sucesso", "success": True, "spotify_data": sp.me()}


@router.get(f"{CONTEXT}/artists/list")
async def list_artists():
    spotify_gen = SpotifyGenerator()
    config = spotify_gen.load_configs()
    return config


@router.get(f"{CONTEXT}/run")
async def run():
    spotify_gen = SpotifyGenerator()
    return spotify_gen.generate()