from fastapi import (
    APIRouter, Depends,
)

from mainApi.auth.auth import get_current_user
from mainApi.images.sub_routers.tile.routers import router as tile_router

router = APIRouter(
    prefix="/image",
    tags=["image"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(tile_router)
