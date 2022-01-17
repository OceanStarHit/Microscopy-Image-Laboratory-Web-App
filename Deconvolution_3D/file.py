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
from mainApi.app.images.utils import functions_3d 
from numpy.core.fromnumeric import shape

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

    return response