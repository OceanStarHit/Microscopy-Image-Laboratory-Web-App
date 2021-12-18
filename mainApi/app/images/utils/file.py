from pathlib import Path
from typing import List

import PIL
from fastapi import UploadFile
import aiofiles
from motor.motor_asyncio import AsyncIOMotorDatabase

from mainApi.app.auth.models.user import UserModelDB, PyObjectId, ShowUserModel
from mainApi.app.images.sub_routers.tile.models import TileModelDB
from mainApi.app.images.utils.folder import get_user_cache_path, clear_path


async def save_upload_file(upload_file: UploadFile, destination: Path, chunk_size: int = 1024) -> None:
    async with aiofiles.open(destination, 'wb') as out_file:
        while content := await upload_file.read(chunk_size):  # async read chunk
            await out_file.write(content)  # async write chunk


async def add_image_tiles(files: List[UploadFile],
                          absolute_client_path: str,
                          clear_previous: bool,
                          current_user: UserModelDB or ShowUserModel,
                          db: AsyncIOMotorDatabase) -> List[TileModelDB]:
    """
    Saves the uploaded tiles to the cache-storage folder/volume under the user_id of the current_user

    Front end should include a validator that checks if the file has already been uploaded and then reject it.
    No validation is done in the backend
    """
    cache_path = get_user_cache_path(user_id=str(current_user.id), directory="tiles")  # get and create tile cache

    if clear_previous:
        # TODO add deletion of files from cache here as well
        clear_path(cache_path)  # clear any previous tiles
        await db['tile-image-cache'].delete_many({'user_id': current_user.id})  # deletes the database entries

    tiles: List[TileModelDB] = []

    for file in files:
        file_path = cache_path.joinpath(file.filename)

        await save_upload_file(upload_file=file, destination=file_path)  # saves file to cache

        width_px, height_px = PIL.Image.open(file.file).size

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