import os
import shutil
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

def get_cache_directory(directory = 'sources'):
    # cache_dir = ROOT_DIR.joinpath("cache-storage").joinpath(directory)
    cache_dir = Path("/cache-storage").joinpath(directory)
    cache_dir.mkdir(parents=True, exist_ok=True)

    return cache_dir

def get_user_cache_directory(user_id, directory = 'tiling'):
    # cache_dir = ROOT_DIR.joinpath("cache-storage").joinpath('user_' + str(user_id)).joinpath(directory)
    cache_dir = Path("/cache-storage").joinpath('user_' + str(user_id)).joinpath(directory)
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))