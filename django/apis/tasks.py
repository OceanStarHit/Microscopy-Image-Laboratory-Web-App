
@csrf_exempt
def stitch(request):
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