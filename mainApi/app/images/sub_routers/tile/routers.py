import asyncio
import concurrent

import pydantic
from PIL import Image
from fastapi.responses import JSONResponse, FileResponse
from fastapi import (
    Request,
    APIRouter,
    Depends,
    status,
    UploadFile,
    File, Form, HTTPException
)
from motor.motor_asyncio import AsyncIOMotorDatabase

from mainApi.app.auth.auth import get_current_user

from typing import List

from mainApi.app.db.mongodb import get_database
from mainApi.app.images.sub_routers.tile.models import AlignNaiveRequest, TileModelDB, AlignedTiledModel
from mainApi.app.images.utils.align_tiles import align_tiles_naive, align_ashlar
from mainApi.app.images.utils.file import save_upload_file, add_image_tiles
from mainApi.app.images.utils.folder import get_user_cache_path, clear_path
from mainApi.app.auth.models.user import UserModelDB, PyObjectId

router = APIRouter(
    prefix="/tile",
    tags=["tile"],
)
@router.post("/upload_image_tiles/", 
        response_description="Upload Image Tiles",
        status_code=status.HTTP_201_CREATED,
        response_model = List[TileModelDB])
async def upload_image_tiles(files: List[UploadFile] = File(...),
                    clear_previous: bool = Form(False),
                    current_user: UserModelDB = Depends(get_current_user),
                    db: AsyncIOMotorDatabase = Depends(get_database)) -> List[TileModelDB]:
    global global_path  
    file_path = await add_image_tiles(files=files, clear_previous=clear_previous, current_user=current_user, db=db) 
    
    return FileResponse(file_path)

@router.get("/list",
            response_description="Upload Image Tiles",
            response_model=List[TileModelDB],
            status_code=status.HTTP_200_OK)
async def get_tile_list(current_user: UserModelDB = Depends(get_current_user),
                        db: AsyncIOMotorDatabase = Depends(get_database)) -> List[TileModelDB]:
    tiles = await db['tile-image-cache'].find({'user_id': current_user.id})["absolute_path"]
    return pydantic.parse_obj_as(List[TileModelDB], tiles)

@router.post("/update",
             response_description="Update Image Tiles",
             status_code=status.HTTP_200_OK)
async def update_tiles(tiles: List[TileModelDB],
                       current_user: UserModelDB = Depends(get_current_user),
                       db: AsyncIOMotorDatabase = Depends(get_database)):
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
                       current_user: UserModelDB = Depends(get_current_user),
                       db: AsyncIOMotorDatabase = Depends(get_database)):
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
        aligned_tiles = await loop.run_in_executor(pool, align_ashlar, tiles,
                                                   "img_r{row:03}_c{col:03}.tif")  # await result

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
