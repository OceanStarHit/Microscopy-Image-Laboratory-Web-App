import asyncio
import concurrent
import math
import os
from datetime import time
from time import sleep

from PIL import Image
import mimetypes

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File
)

from mainApi.auth.auth import get_current_user

from typing import List

from mainApi.images.sub_routers.tile.models import AlignRequest, TileModel, AlignedTiledModel
from mainApi.images.utils.align_tiles import align_tiles_naive
from mainApi.images.utils.file import save_upload_file
from mainApi.images.utils.folder import get_user_cache_path, clear_path
from mainApi.auth.models.user import UserModelDB

router = APIRouter(
    prefix="/tile",
    tags=["tile"],
)


@router.post("/upload_image_tiles",
             response_description="Upload Image Tiles",
             status_code=status.HTTP_200_OK,
             response_model=List[TileModel])
async def upload_image_tiles(files: List[UploadFile] = File(...),
                             current_user: UserModelDB = Depends(get_current_user)) -> List[TileModel]:
    """ Saves the uploaded tiles to the cache-storage folder/volume under the user_id of the current_user """
    cache_path = get_user_cache_path(user_id=str(current_user.id), directory="tiles")  # get and create tile cache
    clear_path(cache_path)  # clear any previous tiles

    tiles: List[TileModel] = []

    for file in files:
        file_path = cache_path.joinpath(file.filename)

        await save_upload_file(upload_file=file, destination=file_path)  # saves file to cache

        width_px, height_px = Image.open(file.file).size

        tile = TileModel(
            absolute_path=str(file_path),
            file_name=file.filename,
            content_type=file.content_type,
            width_px=width_px,
            height_px=height_px
        )

        tiles.append(tile)

    return tiles


@router.get("/list",
            response_description="Upload Image Tiles",
            response_model=List[TileModel],
            status_code=status.HTTP_200_OK)
async def get_uploaded_tile_list(current_user: UserModelDB = Depends(get_current_user)) -> List[TileModel]:

    cache_path = get_user_cache_path(user_id=str(current_user.id), directory="tiles")  # get and create tile cache

    tile_path_list = [cache_path.joinpath(f) for f in os.listdir(cache_path) if
                      os.path.isfile(cache_path.joinpath(f)) or os.path.islink(cache_path.joinpath(f))]

    tiles: List[TileModel] = []

    for file_path in tile_path_list:
        width_px, height_px = Image.open(file_path).size  # this is the slow bit

        mimetype = mimetypes.MimeTypes().guess_type(os.path.basename(file_path))[0]

        tile = TileModel(
            absolute_path=str(file_path),
            file_name=os.path.basename(file_path),
            content_type=mimetype,
            width_px=width_px,
            height_px=height_px
        )

        tiles.append(tile)

    return tiles


@router.get("/align_tiles",
            response_description="Align Tiles",
            response_model=List[AlignedTiledModel],
            status_code=status.HTTP_200_OK)
async def align_tiles(request: AlignRequest,
                      tiles: List[TileModel] = Depends(get_uploaded_tile_list)) -> List[AlignedTiledModel]:
    """
        performs a naive aligning of the tiles simply based on the given rows and method.
        does not perform any advanced stitching or pixel checking

        Called using concurrent.futures to make it async
    """

    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        aligned_tiles = await loop.run_in_executor(pool, align_tiles_naive, request, tiles)  # await result
        return aligned_tiles



@router.get("/export_stitched_image",
            response_description="Export stitched Image",
            response_model=List[AlignedTiledModel],
            status_code=status.HTTP_200_OK)
# async def export_stitched_image(tiles: List[AlignedTiledModel]) -> List[TileModel]:
async def export_stitched_image() -> List[TileModel]:
    """ This is meant to called after the images are aligned, so it takes a list of AlignedTiledModel in the body """
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)  # wait result
        print(result)
