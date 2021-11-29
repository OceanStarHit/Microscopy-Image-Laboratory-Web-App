import math
import time
from typing import List

from mainApi.images.sub_routers.tile.models import AlignRequest, AlignedTiledModel, TileModel


def align_tiles_naive(request: AlignRequest,
                      tiles: List[TileModel]) -> List[AlignedTiledModel]:
    """
        performs a naive aligning of the tiles simply based on the given rows and method.
        does not perform any advanced stitching or pixel checking.

        Meant to be called in a separate thread due it being cpu bound.
    """
    time.sleep(30)

    if len(tiles) == 0:
        return []

    # assumes they are all the same size
    width_px = tiles[0].width_px
    height_px = tiles[0].height_px

    columns = math.ceil(len(tiles) / request.rows)

    row = 0
    col = 0

    aligned_tiles: List[AlignedTiledModel] = []

    for index, tile in enumerate(tiles):
        if request.method == "byRow":
            col = index % columns
        else:
            row = index % request.rows

        tile = tile.dict()
        tile["x"] = col * width_px
        tile["y"] = row * height_px

        aligned_tiles.append(AlignedTiledModel.parse_obj(tile))

        if request.method == "byRow":
            if col == columns - 1:
                row = row + 1
        else:
            if row == request.rows - 1:
                col = col + 1

    return aligned_tiles
