from pathlib import Path
from typing import List
import os
import PIL
from skimage import io
import numpy as np
import datetime
from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
from mainApi.app.auth.models.user import UserModelDB, PyObjectId, ShowUserModel
from mainApi.app.images.sub_routers.tile.models import TileModelDB
from mainApi.app.images.utils.folder import get_user_cache_path, clear_path
from mainApi.app import main
from mainApi.config import STATIC_PATH
from mainApi.app.images.utils import functions 
from numpy.core.fromnumeric import shape

def convol2D_processing(file, path):
    displayed_dir = path
    current_image_array = file
    current_time = datetime.datetime.now() 
    time_str = current_time.strftime("%Y%m%d_%H%M%S")

    print('Deconvolving 2D')
    print(current_image_array.shape)

    if len(current_image_array.shape)==2:
        functions.remove_png_files(displayed_dir)
        path_images = []        
        current_image_array = functions.Deconvolve(current_image_array)
        displayed_image_array = functions.normalize_2Dim_uint8(current_image_array)
        path_image = os.path.join(displayed_dir, 'slice_000_'+ time_str +'.png')
        io.imsave( path_image, displayed_image_array)
        path_image = path_image.split("/")[-1]
        path_images.append(path_image)
        response = {
            '3D_flag': False,
            'N_images': 1,
            'path_images': path_images,
        }

    elif len(current_image_array.shape)==3 and current_image_array.shape[2] in [3,4]:
        functions.remove_png_files(displayed_dir)
        path_images = []
        displayed_image_array = np.zeros_like(current_image_array)
        N_images = current_image_array.shape[2]
        for i in range(N_images):
            displayed_image_array[:,:,i] = functions.Deconvolve(current_image_array[:,:,i])
        path_image = os.path.join(displayed_dir, 'slice_{num:03d}'.format(num=i)+ '_' + time_str + '.png')
        io.imsave(path_image, displayed_image_array.astype(np.uint8))
        path_image = path_image.split("/")[-1]
        path_images.append(path_image)
        current_image_array = displayed_image_array       
        response = {
            '3D_flag': False,
            'N_images': 1,
            'path_images': path_images,
        }
    
    elif len(current_image_array.shape)==3 and current_image_array.shape[2] not in [3,4]:
        functions.remove_png_files(displayed_dir)
        path_images = []        
        displayed_image_array = np.zeros_like(current_image_array)
        N_images = current_image_array.shape[0]
        for i in range(N_images):
            displayed_image_array[i] = functions.Deconvolve(current_image_array[i])
            displayed_image = functions.normalize_2Dim_uint8(displayed_image_array[i])
            path_image = os.path.join(displayed_dir, 'slice_{num:03d}'.format(num=i)+ '_' + time_str + '.png')
            io.imsave(path_image, displayed_image)
            path_image = path_image.split("/")[-1]
            path_images.append(path_image)
        current_image_array = displayed_image_array

        response = {
            '3D_flag': True,
            'N_images': N_images,
            'path_images': path_images,
        }

    else:
        response = {
            '3D_flag': True,
            'N_images': 0,
            'path_images': None,
        }
    print("2D Deconvolution was finished!")
    return response

def convol3D_processing(file, path):
    current_image_array = file
    displayed_dir = path
    current_time = datetime.datetime.now() 
    time_str = current_time.strftime("%Y%m%d_%H%M%S")
    path_images = []        
    if len(current_image_array.shape)==3 and current_image_array.shape[2] not in [3,4]:
        functions.remove_png_files(displayed_dir)
        path_images = []        

        print('Deconvolving 3D')
        print(current_image_array.shape)

        current_image_array = functions.Deconvolve(current_image_array)
        N_images = current_image_array.shape[0]
        for i in range(N_images):
            path_image = os.path.join(displayed_dir, 'slice_{num:03d}'.format(num=i) + '_' + time_str + '.png')
            displayed_image_array = functions.normalize_2Dim_uint8(current_image_array[i])
            io.imsave(path_image, displayed_image_array)
            path_image = path_image.split("/")[-1]
            path_images.append(path_image)

        response = {
            '3D_flag': True,
            'N_images': N_images,
            'path_images': path_images,
        }

    else:
        # current_image_array = None
        response = {
            '3D_flag': False,
            'N_images': 0,
            'path_images': None,
        }

    print("3D Deconvolution was finished!")
    return response

async def add_image_tiles(path: Path,
                            files: List[UploadFile],
                          clear_previous: bool,
                          current_user: UserModelDB or ShowUserModel,
                          db: AsyncIOMotorDatabase) -> List[TileModelDB]:
    """
    Saves the uploaded tiles to the cache-storage folder/volume under the user_id of the current_user

    Front end should include a validator that checks if the file has already been uploaded and then reject it.
    No validation is done in the backend
    """
    cache_path = STATIC_PATH
    raw_source = io.imread(path)
    image_num = raw_source.shape    
    current_time = datetime.datetime.now() 
    time_str = current_time.strftime("%Y%m%d_%H%M%S")
    path_images = []
    if image_num[2] > 3:
        for i in range(image_num[0]):
            path_image = os.path.join(cache_path, 'slice_{num:03d}'.format(num=i)+ '_' + time_str + '.png')
            io.imsave(path_image, normalize_2Dim_uint8(raw_source[i]))
            path_image = path_image.split('/')[-1]
            path_images.append(path_image)
        D_flag = True
        return D_flag, image_num[0], path_images

    else:
        tiles: List[TileModelDB] = []
        file = files[0]
        path_image = os.path.join(cache_path, 'slice_000_'+ time_str +'.png')
        io.imsave(path_image, normalize_2Dim_uint8(raw_source))
        path_image = path_image.split('/')[-1]
        path_images.append(path_image)
        width_px, height_px = PIL.Image.open(file.file).size
        tile = TileModelDB(
            user_id=PyObjectId(current_user.id),
            absolute_path=str(path),
            file_name=file.filename,
            content_type=file.content_type,
            width_px=width_px,
            height_px=height_px
        )
        tiles.append(tile)
        await db['tile-image-cache'].insert_many([t.dict(exclude={'id'}) for t in tiles])
        path = tiles[0].absolute_path
        D_flag = False
        image_num = 1

        return D_flag, image_num, path_images
        
def normalize_2Dim_uint8(im):
    im = im.astype(np.float32)
    min = np.min(im)
    max = np.max(im)
    im = (im-min)/(max-min)*255
    return im.astype(np.uint8)