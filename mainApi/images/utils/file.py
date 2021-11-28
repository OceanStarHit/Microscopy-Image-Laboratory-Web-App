from pathlib import Path
from fastapi import UploadFile
import aiofiles

async def save_upload_file(upload_file: UploadFile, destination: Path, chunk_size: int = 1024) -> None:
    async with aiofiles.open(destination, 'wb') as out_file:
        while content := await upload_file.read(chunk_size):  # async read chunk
            await out_file.write(content)  # async write chunk

