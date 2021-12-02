import asyncio
import concurrent

import pydantic
from PIL import Image

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File, Form, HTTPException
)

from celery_tasks.tasks import StitchingCeleryTask
from celery_tasks.utils import create_worker_from
from mainApi.auth.auth import get_current_user

from typing import List

from mainApi.config import get_db

from mainApi.images.sub_routers.tile.models import AlignNaiveRequest, TileModelDB, AlignedTiledModel
from mainApi.images.utils.align_tiles import align_tiles_naive, align_ashlar
from mainApi.images.utils.file import save_upload_file
from mainApi.images.utils.folder import get_user_cache_path, clear_path
from mainApi.auth.models.user import UserModelDB, PyObjectId

router = APIRouter(
    prefix="/tile",
    tags=["tile"],
)

db = get_db()

@router.post("/upload_image_tiles",
             response_description="Upload Image Tiles",
             status_code=status.HTTP_200_OK,
             response_model=List[TileModelDB])
async def upload_image_tiles(files: List[UploadFile] = File(...),
                             clear_previous: bool = Form(True),
                             current_user: UserModelDB = Depends(get_current_user)) -> List[TileModelDB]:
    """
    Saves the uploaded tiles to the cache-storage folder/volume under the user_id of the current_user

    Front end should include a validator that checks if the file has already been uploaded and then reject it.
    No validation is done in the backend
    """
    cache_path = get_user_cache_path(user_id=str(current_user.id), directory="tiles")  # get and create tile cache

    if clear_previous:
        clear_path(cache_path)  # clear any previous tiles
        await db['tile-image-cache'].delete_many({'user_id': current_user.id})  # deletes the database entries

    tiles: List[TileModelDB] = []

    for file in files:
        file_path = cache_path.joinpath(file.filename)

        await save_upload_file(upload_file=file, destination=file_path)  # saves file to cache

        width_px, height_px = Image.open(file.file).size

        tile = TileModelDB(
            user_id=PyObjectId(current_user.id),
            absolute_path=str(file_path),
            file_name=file.filename,
            content_type=file.content_type,
            width_px=width_px,
            height_px=height_px
        )

        tiles.append(tile)

    await db['tile-image-cache'].insert_many([t.dict(exclude={'id'}) for t in tiles])

    return tiles


@router.get("/list",
            response_description="Upload Image Tiles",
            response_model=List[TileModelDB],
            status_code=status.HTTP_200_OK)
async def get_tile_list(current_user: UserModelDB = Depends(get_current_user)) -> List[TileModelDB]:
    tiles = await db['tile-image-cache'].find({'user_id': current_user.id}).to_list(None)
    return pydantic.parse_obj_as(List[TileModelDB], tiles)


@router.post("/update",
             response_description="Update Image Tiles",
             status_code=status.HTTP_200_OK)
async def update_tiles(tiles: List[TileModelDB],
                       current_user: UserModelDB = Depends(get_current_user)):
    # make sure we are not trying to alter any tiles we do not own
    # we check this first and if they are trying to update any un owned docs we dont update any
    for tile in tiles:
        if tile.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot update tile that does not belong to user",
                headers={"WWW-Authenticate": "Bearer"},
            )

    for tile in tiles:
        result = await db['tile-image-cache'].replace_one({'_id': tile.id}, tile.dict(exclude={'id'}))


@router.post("/delete",
             response_description="Update Image Tiles",
             status_code=status.HTTP_200_OK)
async def delete_tiles(tiles: List[TileModelDB],
                       current_user: UserModelDB = Depends(get_current_user)):
    # make sure we are not trying to delete any tiles we do not own
    # we check this first and if they are trying to delete any un owned docs we dont update any
    for tile in tiles:
        if tile.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot update tile that does not belong to user",
                headers={"WWW-Authenticate": "Bearer"},
            )

    results = []

    for tile in tiles:
        result = await db['tile-image-cache'].delete_one({'_id': tile.id})
        results.append(result)

    return results


@router.get("/align_tiles_naive",
            response_description="Align Tiles",
            response_model=List[AlignedTiledModel],
            status_code=status.HTTP_200_OK)
async def _align_tiles_naive(request: AlignNaiveRequest,
                             tiles: List[TileModelDB] = Depends(get_tile_list)) -> List[AlignedTiledModel]:
    """
        performs a naive aligning of the tiles simply based on the given rows and method.
        does not perform any advanced stitching or pixel checking

        Called using concurrent.futures to make it async
    """

    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        aligned_tiles = await loop.run_in_executor(pool, align_tiles_naive, request, tiles)  # await result

        return aligned_tiles


@router.get("/align_tiles_ashlar",
            response_description="Align Tiles",
            # response_model=List[AlignedTiledModel],
            status_code=status.HTTP_200_OK)
async def _align_tiles_ashlar(tiles: List[TileModelDB] = Depends(get_tile_list)) -> any:
    """
        performs a naive aligning of the tiles simply based on the given rows and method.
        does not perform any advanced stitching or pixel checking

        Called using concurrent.futures to make it async
    """

    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        aligned_tiles = await loop.run_in_executor(pool, align_ashlar, tiles, "img_r{row:03}_c{col:03}.tif")  # await result

        return aligned_tiles


@router.get("/export_stitched_image",
            response_description="Export stitched Image",
            response_model=List[AlignedTiledModel],
            status_code=status.HTTP_200_OK)
# async def export_stitched_image(tiles: List[AlignedTiledModel]) -> List[TileModel]:
async def export_stitched_image() -> List[TileModelDB]:
    """ This is meant to called after the images are aligned, so it takes a list of AlignedTiledModel in the body """
    pass
    # loop = asyncio.get_event_loop()
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, cpu_bound)  # wait result
    #     print(result)
