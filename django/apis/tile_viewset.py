from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from apis.custom_bioformats import utils
from os.path import exists
import json
from PIL import Image
import math
import numpy as np
import cv2 as cv
import subprocess
from django.http import FileResponse
import logging
from celery_tasks.tasks import StitchingCeleryTask
from celery_tasks.utils import create_worker_from

"""
Get the list of uploaded files
curl -X GET http://127.0.0.1:8000/apis/tiles/ -H 'Authorization: Token {token_value}'

Align the tiles on the canvas
curl -X POST http://127.0.0.1:8000/apis/tiles/align/ -H 'Authorization: Token {token_value}' -d "row=4&method=byRow"

Download the tiled image
curl -X GET http://127.0.0.1:8000/apis/tiles/export/ -H 'Authorization: Token {token_value}' --output ~/Downloads/aa.png

"""

# create worker
_, stitching_worker = create_worker_from(StitchingCeleryTask)

logger = logging.getLogger(__name__)


def getWorkingFolder(user_id):
    return utils.get_user_cache_directory(user_id, TileViewSet.CACHE_FOLDER)


def getTileList(user_id):
    working_folder = getWorkingFolder(user_id)
    json_path = working_folder.joinpath(TileViewSet.META_JSON)
    if exists(json_path):
        with open(json_path, 'r') as json_file:
            json_object = json.load(json_file)

        for item in json_object:
            if "x" not in item:
                item["x"] = 0
            if "y" not in item:
                item["y"] = 0
            if "width" not in item:
                item["width"] = 0
            if "height" not in item:
                item["height"] = 0
        return json_object
    return []


def saveTileList(user_id, tiles):
    working_folder = getWorkingFolder(user_id)
    json_path = working_folder.joinpath(TileViewSet.META_JSON)
    json_object = json.dumps(tiles)
    with open(json_path, 'w+') as json_file:
        json_file.write(json_object)


class TileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    META_JSON = "meta.json"
    CACHE_FOLDER = "tiling"

    def list(self, request):
        tile_list = getTileList(request.user.id)

        return Response(tile_list)

    def create(self, request):
        return Response(status=200)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    @action(detail=False, methods=['post'])
    def batch_create(self, request):
        working_folder = getWorkingFolder(request.user.id)

        utils.clear_folder(working_folder)
        if "files" in request.FILES:
            files = request.FILES.getlist("files")
            metadata_list = []
            for i, f in enumerate(files):
                full_path = working_folder.joinpath(f.name)
                metadata = {
                    "file_name": f.name,
                    "path": str(full_path),
                    "id": i + 1
                }
                with open(full_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                metadata_list.append(metadata)

            saveTileList(request.user.id, metadata_list)

        return Response(status=200)

    @action(detail=False, methods=['post'])
    def align(self, request):
        total_row = 1
        method = "byRow"

        if "row" in request.POST:
            total_row = int(request.POST["row"])
            if total_row == 0:
                total_row = 1
        if "method" in request.POST:
            method = request.POST["method"]

        logger.info("method: " + method + " total_row: " + str(total_row))

        tiles = getTileList(request.user.id)
        if len(tiles) == 0:
            return Response(status=200)

        width, height = Image.open(tiles[0]["path"]).size

        total_col = math.ceil(len(tiles) / total_row)

        row = 0
        col = 0
        for i, t in enumerate(tiles):
            if method == "byRow":
                col = i % total_col
            else:
                row = i % total_row

            # print(str(row) + ", " + str(col))

            t["x"] = col * width
            t["y"] = row * height
            t["width"] = width
            t["height"] = height

            if method == "byRow":
                if col == total_col - 1:
                    row = row + 1
            else:
                if row == total_row - 1:
                    col = col + 1

        saveTileList(request.user.id, tiles)

        return Response(status=200)

    @action(detail=True, methods=['get'])
    def stitch(self, request, pk=None):
        print("-----stitch")
        stitching_worker.apply_async(args=[request, ])

        print(pk)
        print("-----")
        return Response(status=200)

    @action(detail=False, methods=['post'])
    def auto_stitch(self, request):
        return Response(status=200)

    @action(detail=False, methods=['get'])
    def export(self, request):
        tiles = getTileList(request.user.id)
        if len(tiles) > 0:
            example = tiles[0]
            img = cv.imread(example["path"], cv.IMREAD_COLOR)
            # cv.imshow("Cute Kitens", img)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

            height = img.shape[0]
            width = img.shape[1]
            channel = img.shape[2]

            max_x = 0
            max_y = 0
            for t in tiles:
                if t["x"] > max_x:
                    max_x = t["x"]
                if t["y"] > max_y:
                    max_y = t["y"]

            total_width = max_x + width
            total_height = max_y + height
            video_size = str(total_width) + "x" + str(total_height)
            print(video_size + " CH: " + str(channel))
            emptyFileSize = total_width * total_height * channel
            print("Total file size: " + str(emptyFileSize))

            # 5G uppper limit
            if emptyFileSize < 100000000000:
                working_folder = getWorkingFolder(request.user.id)
                raw_file = working_folder.joinpath("tiling_result.raw")
                png_file = working_folder.joinpath("tiling_result.png")

                with open(raw_file, "wb") as f:
                    f.seek(emptyFileSize - 1)
                    f.write(b"\0")

                    for t in tiles:
                        # write rgb data to file
                        img = cv.imread(t["path"])
                        for row in range(img.shape[0]):
                            x = t["x"]
                            y = t["y"] + row

                            pos = (y * total_width + x) * channel

                            # logger.debug(len(img[row]))
                            row_data = img[row].flatten()
                            # logger.debug(len(row_data))
                            # logger.debug(row_data)
                            f.seek(pos)
                            f.write(row_data)

                imagematic_cmd = [
                    "convert",
                    "-depth",
                    "8",
                    "-size",
                    video_size,
                    "BGR:" + str(raw_file),
                    str(png_file)
                ]
                # logger.debug(imagematic_cmd)
                subprocess.run(imagematic_cmd)

                img = open(png_file, 'rb')
                response = FileResponse(img)
                return response

        return Response(status=422)
