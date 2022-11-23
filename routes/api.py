from fastapi import APIRouter

from routes import root, generator
API_CONTEXT = "/api"

router = APIRouter()
router.include_router(root.router, tags=["root"])
router.include_router(generator.router, tags=["generator"], prefix=f"{API_CONTEXT}")
