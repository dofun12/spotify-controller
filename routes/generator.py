from fastapi import APIRouter

from generator.spotify_generator import SpotifyGenerator

router = APIRouter()

CONTEXT = "/generator"


@router.get(f"{CONTEXT}/")
async def generate():
    return {"message": "Hello World"}


@router.get(f"{CONTEXT}/artistists/list")
async def list_artistis():
    spotify_gen = SpotifyGenerator()
    config = spotify_gen.load_configs()
    return config
