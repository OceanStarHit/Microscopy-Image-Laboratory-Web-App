"""
Script file: apis.py
Created on: Feb 25, 2021
Last modified on: Mar 28, 2021

Comments:
    Django API endpoint definition
"""

import json
import cv2
import numpy as np

from http import HTTPStatus
from pathlib import Path
from base64 import b64encode, b64decode
from uuid import uuid4
from subprocess import call
from traceback import print_exc
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse

from .custom_bioformats import ImageInfo, utils


current_data = None

######################
# Endpoint Functions #
######################

@csrf_exempt
def set_image(request):
    global current_data

    try:
        source_image = request.FILES.get('sourceImage')
        
        if utils.check_source_format(source_image):
            source_file = utils.save_source_image(source_image)

            imageInfo = ImageInfo(source_file)
            ret = imageInfo.parse_by_bioformat(show_log=True)
            
            if ret:
                current_data = imageInfo

                first_image = imageInfo.get_first_image()
                return JsonResponse(first_image, status=HTTPStatus.OK)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Invalid image data',
                }, status=HTTPStatus.NOT_ACCEPTABLE)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Invalid image type',
            }, status=HTTPStatus.NOT_ACCEPTABLE)
    except Exception:
        return response_error()

@csrf_exempt
def set_metadata(request):

    jsonReq = request.FILES
    jsonRes = {}
    for key in jsonReq:

        try:
            metadata = jsonReq[key]

            if utils.check_source_format(metadata):
                metafile = utils.save_source_image(metadata)

                metaInfo = ImageInfo(metafile)
                ret = metaInfo.parse_by_bioformat(show_log=True)
                
                if ret:
                    jsonRes[key] = metaInfo.get_first_image()
                else:
                    jsonRes[key] = None
            else:
                jsonRes[key] = None
        except Exception:
            jsonRes[key] = None

    return JsonResponse(jsonRes, status=HTTPStatus.OK)

@csrf_exempt
def change_image(request):
    global current_data

    try:
        req_json = json.loads(request.body.decode("utf-8"))
        image_id = req_json['imageId']

        result = current_data.change_image(image_id - 1)
        return JsonResponse(result, status=HTTPStatus.OK)
    except Exception:
        return response_error()

@csrf_exempt
def change_parameter(request):
    global current_data

    try:
        req_json = json.loads(request.body.decode("utf-8"))

        Z = req_json['Z']
        T = req_json['T']
        C = req_json['C']

        result = current_data.change_tzc(T - 1, Z - 1, C)
        return JsonResponse(result, status=HTTPStatus.OK)
    except Exception:
        return response_error()

@csrf_exempt
def adjust_image(request):
    try:
        req_json = json.loads(request.body.decode("utf-8"))

        base64image = req_json['imageData']
        raw_data = b64decode(base64image[22:])
        brightness = req_json['brightness']
        contrast = req_json['contrast']
        gamma = req_json['gamma']

        image_file = utils.save_processing_file(raw_data)

        changed_file = utils.change_image_parameter(image_file, brightness, contrast, gamma)
        image_data = utils.make_image_data(changed_file)
        result = {'imageData': image_data}

        return JsonResponse(result, status=HTTPStatus.OK)
    except Exception:
        return response_error()

@csrf_exempt
def color_channel(request):
    try:
        base64image = request.POST.get('image')
        raw_data = b64decode(base64image[22:])
        channels = request.POST.get('channels')

        image_file = utils.save_processing_file(raw_data)

        if channels == 's':
            image_data = utils.make_image_data(image_file)
        else:
            channels_file = utils.split_channels(image_file, channels)
            image_data = utils.make_image_data(channels_file)
            
            # utils.delete_file(channels_file)

        return JsonResponse({
                    'status': True,
                    'data': image_data,
                }, status=HTTPStatus.OK)
    except Exception:
        return response_error()

@csrf_exempt
def gray(request):
    try:
        base64image = request.POST.get('image')
        raw_data = b64decode(base64image[22:])
        bits = request.POST.get('bits')

        image_file = utils.save_processing_file(raw_data)

        gray_file = utils.convert_to_gray(image_file, bits)
        image_data = utils.make_image_data(gray_file)

        # utils.delete_file(gray_file)

        return JsonResponse({
                    'status': True,
                    'data': image_data,
                }, status=HTTPStatus.OK)
    except Exception:
        return response_error()

# @csrf_exempt
# def change_parameter(request):
#     try:
#         base64image = request.POST.get('image')
#         raw_data = b64decode(base64image[22:])
#         brightness = float(request.POST.get('brightness'))
#         contrast = float(request.POST.get('contrast'))
#         gamma = float(request.POST.get('gamma'))

#         image_file = utils.save_processing_file(raw_data)

#         changed_file = utils.change_image_parameter(image_file, brightness, contrast, gamma)
#         image_data = utils.make_image_data(changed_file)

#         # utils.delete_file(changed_file)

#         return JsonResponse({
#                     'status': True,
#                     'data': image_data,
#                 }, status=HTTPStatus.OK)
#     except Exception:
#         return response_error()
    
# @csrf_exempt
def equalize(request):
    """ヒストグラム平坦化関数"""

    # キャッシュディレクトリを作成
    cache_dir = Path(__file__).parent.joinpath('cache').joinpath('equalize')
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 画像データをbase64形式で取得
    base64image = request.POST.get('image')
    # base64をバイナリデータに変換し、ヘッダーも同時に保存する
    if base64image.startswith('data:image/png;'):
        raw_image = b64decode(base64image[22:])
        header = 'data:image/png;base64,'
    elif base64image.startswith('data:image/gif;'):
        raw_image = b64decode(base64image[22:])
        header = 'data:image/gif;base64,'
    elif base64image.startswith('data:image/jpeg;'):
        raw_image = b64decode(base64image[23:])
        header = 'data:image/jpeg;base64,'
    # ファイル名生成
    if base64image.startswith('data:image/png;'):
        file_name = str(cache_dir.joinpath(uuid4().hex + '.png'))
    elif base64image.startswith('data:image/jpeg;'):
        file_name = str(cache_dir.joinpath(uuid4().hex + '.jpg'))
    elif base64image.startswith('data:image/gif;'):
        file_name = str(cache_dir.joinpath(uuid4().hex + '.gif'))
    else:
        return HttpResponse('UnknownType')
    # 画像をキャッシュディレクトリに保存
    with open(file_name, mode='wb') as file:
        file.write(raw_image)
    # cv2による画像読み込み
    img = cv2.imread(file_name,1)
    # 画像をRGBからグレースケールに変更
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 処理できる形式に変更
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    # 処理開始
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    hist_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    # 処理後の画像を保存
    cv2.imwrite(file_name + '-hist', hist_img)
    # 変更後の画像をbase64形式で返す。
    with open(file_name + '-hist', mode='rb') as file:
        raw_new_image = file.read()
        base64_new_image = b64encode(raw_new_image)
        return HttpResponse(header + base64_new_image.decode())

####################
# Helper Functions #
####################

def response_error():
    print_exc()
    return JsonResponse({
            'status': False,
            'message': 'Server Error',
        }, status=HTTPStatus.INTERNAL_SERVER_ERROR)