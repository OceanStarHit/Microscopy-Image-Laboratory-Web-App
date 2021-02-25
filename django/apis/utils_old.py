import os
import threading
from pathlib import Path
from uuid import uuid4
from base64 import b64encode, b64decode
from subprocess import call
from traceback import print_exc

import cv2
import numpy as np

import javabridge
import bioformats

# from .bioformats import formatreader as fr

import imageio

#####################
# Generic Functions #
#####################

def get_cache_directory(directory = 'sources'):
    cache_dir = Path(__file__).parent.joinpath('cache').joinpath(directory)
    cache_dir.mkdir(parents=True, exist_ok=True)

    return cache_dir

def base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode()

def make_image_data(image_path):
    return 'data:image/png;base64,' + base64_encoded_image(image_path)

def check_source_format(source_image):
    # available format - 181
    available_formats = ['.1sc', '.2', '.2fl', '.3', '.4', '.acff', '.afi', '.afm', '.aim', '.al3d', '.ali', '.am', '.amiramesh', '.apl', '.arf', '.avi', '.bif', '.bin', '.bip', '.bmp', '.btf', '.c01', '.cfg', '.ch5', '.cif', '.cr2', '.crw', '.csv', '.cxd', '.czi', '.dat', '.dcm', '.dib', '.dicom', '.dm2', '.dm3', '.dm4', '.dti', '.dv', '.eps', '.epsi', '.exp', '.fdf', '.fff', '.ffr', '.fits', '.flex', '.fli', '.frm', '.gel', '.gif', '.grey', '.h5', '.hdf', '.hdr', '.hed', '.his', '.htd', '.html', '.hx', '.i2i', '.ics', '.ids', '.im3', '.img', '.ims', '.inr', '.ipl', '.ipm', '.ipw', '.j2k', '.jp2', '.jpf', '.jpg', '.jpk', '.jpx', '.klb', '.l2d', '.labels', '.lei', '.lif', '.liff', '.lim', '.lms', '.lsm', '.map', '.mdb', '.mea', '.mnc', '.mng', '.mod', '.mov', '.mrc', '.mrcs', '.mrw', '.msr', '.mtb', '.mvd2', '.naf', '.nd', '.nd2', '.ndpi', '.ndpis', '.nef', '.nhdr', '.nii', '.nii.gz', '.nrrd', '.obf', '.obsep', '.oib', '.oif', '.oir', '.ome', '.ome.btf', '.ome.tf2', '.ome.tf8', '.ome.tif', '.ome.tiff', '.ome.xml', '.par', '.pbm', '.pcoraw', '.pcx', '.pds', '.pgm', '.pic', '.pict', '.png', '.pnl', '.ppm', '.pr3', '.ps', '.psd', '.qptiff', '.r3d', '.raw', '.rcpnl', '.rec', '.res', '.scn', '.sdt', '.seq', '.sif', '.sld', '.sm2', '.sm3', '.spc', '.spe', '.spi', '.st', '.stk', '.stp', '.svs', '.sxm', '.tf2', '.tf8', '.tfr', '.tga', '.tif', '.tiff', '.tnb', '.top', '.txt', '.v', '.vff', '.vms', '.vsi', '.vws', '.wat', '.wlz', '.wpi', '.xdce', '.xml', '.xqd', '.xqf', '.xv', '.xys', '.zfp', '.zfr', '.zvi']
    _, file_extension = os.path.splitext(source_image.name)

    try:
        available_formats.index(file_extension.lower())
        return True
    except Exception:
        print_exc()
        return False

def save_source_image(source_image):
    dest_dir = get_cache_directory()

    _, file_extension = os.path.splitext(source_image.name)
    file_path = str(dest_dir.joinpath(uuid4().hex + file_extension))

    with open(file_path, mode='wb') as destination:
        for chunk in source_image.chunks():
            destination.write(chunk)
    
    return file_path

def save_processing_file(raw_data):
    dest_dir = get_cache_directory('raw_data')
    file_path = str(dest_dir.joinpath(uuid4().hex + '.png'))

    with open(file_path, mode='wb') as destination:
        destination.write(raw_data)
    
    return file_path

def is_tiff(source_file):
    _, file_extension = os.path.splitext(source_file)

    return file_extension.lower() == '.tif' or file_extension.lower() == '.tiff'

def exec_command(shell_script):
    call(shell_script, shell=True)

def convert_to_png(source_file):
    dest_dir = get_cache_directory('converted')
    file_name, _ = os.path.splitext(os.path.basename(source_file))
    converted_file = str(dest_dir.joinpath(file_name + '.png'))

    exec_command(f'gm convert {source_file} {converted_file}')

    return converted_file

def save_image(image_array, scale):
    dest_dir = get_cache_directory('bioformats')
    saved_file = str(dest_dir.joinpath(uuid4().hex + '.png'))

    print(image_array)
    print(f'Scale: {scale}')

    image_size = image_array.shape
    print(image_size)

    if (len(image_size) == 3 and image_size[2] == 2):
        imageio.imwrite(saved_file, image_array[:, :, 0])
    else:
        imageio.imwrite(saved_file, image_array)

    return saved_file

# def save_image(image_array, meta):
#     dest_dir = get_cache_directory('bioformats')
#     saved_file = str(dest_dir.joinpath(uuid4().hex + '.png'))
    
#     if not meta['PixelType'] is None:
#         pixel_type = meta['PixelType']
#     else:
#         pixel_type = 0

#     # print(image_array)
#     # print(image_array.dtype)
#     # print(pixel_type)
    
#     if pixel_type == 0 or pixel_type == 1:
#         im = Image.fromarray(np.uint8(image_array))
#     else:
#         scaled = (image_array - image_array.min()) / (image_array.max() - image_array.min()) * 255
#         im = Image.fromarray(np.uint8(scaled)).convert("RGB")

#     im.save(saved_file)

#     return saved_file

def delete_file(file):
    t = threading.Thread(target=delete_file_thread, args=[file], daemon=True)
    t.start()

def delete_file_thread(file):
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist")


####################
# OpenCV Functions #
####################

def split_channels(image_file, channels):
    origin_img = cv2.imread(image_file, 1)

    if len(origin_img.shape) == 3:
        height, width, _ = origin_img.shape[:3]
    else:
        height, width = origin_img.shape[:2]

    zeros = np.zeros((height, width), origin_img.dtype)
    # B, G, R
    blue_ch, green_ch, red_ch = cv2.split(origin_img)
    
    if channels == 'b':
        img = cv2.merge((blue_ch, zeros, zeros))
    elif channels == 'g':
        img = cv2.merge((zeros, green_ch, zeros))
    elif channels == 'r':
        img = cv2.merge((zeros, zeros, red_ch))
    elif channels == 'bg' or channels == 'gb':
        img = cv2.merge((blue_ch, green_ch, zeros))
    elif channels == 'br' or channels == 'rb':
        img = cv2.merge((blue_ch, zeros, red_ch))
    elif channels == 'gr' or channels == 'rg':
        img = cv2.merge((zeros, green_ch, red_ch))
    else:
        img = cv2.merge((blue_ch, green_ch, red_ch))

    dest_dir = get_cache_directory('channels')
    new_image_file = str(dest_dir.joinpath(uuid4().hex + '.png'))
    
    cv2.imwrite(new_image_file, img)

    return new_image_file

def convert_to_gray(image_file, bits):
    origin_img = cv2.imread(image_file)

    img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

    if bits == '8':
        img = map_uint16_to_uint8(map_uint16_to_uint8(img))
    elif bits == '16':
        img = map_uint16_to_uint8(img)

    dest_dir = get_cache_directory('gray')
    new_image_file = str(dest_dir.joinpath(uuid4().hex + '.png'))
    
    cv2.imwrite(new_image_file, img)

    return new_image_file

def map_uint16_to_uint8(img, lower_bound=None, upper_bound=None):
    if lower_bound is not None and not(0 <= lower_bound < 2**16):
        raise ValueError(
            '"lower_bound" must be in the range [0, 65535]')
    if upper_bound is not None and not(0 <= upper_bound < 2**16):
        raise ValueError(
            '"upper_bound" must be in the range [0, 65535]')
    if lower_bound is None:
        lower_bound = np.min(img)
    if upper_bound is None:
        upper_bound = np.max(img)
    if lower_bound >= upper_bound:
        raise ValueError(
            '"lower_bound" must be smaller than "upper_bound"')

    lut = np.concatenate([
        np.zeros(lower_bound, dtype=np.uint16),
        np.linspace(0, 255, upper_bound - lower_bound).astype(np.uint16),
        np.ones(2**16 - upper_bound, dtype=np.uint16) * 255
    ])
    return lut[img].astype(np.uint8)

def change_image_parameter(image_file, brightness, contrast, gamma):
    dest_dir = get_cache_directory('parameter')
    file_name, _ = os.path.splitext(image_file)
    changed_file = str(dest_dir.joinpath(file_name + '.png'))

    contrast_num = round((50 - round(contrast)) / 10)
    if contrast_num < 0:
        contrast_num = -contrast_num

    if 50 - round(contrast) > 0:
        prefix = '+'
    else:
        prefix = '-'

    script = f'gm convert {image_file} -modulate {brightness + 50} -gamma {(gamma / 25) + 1} {"" if 50 == round(contrast) else " ".join([prefix + "contrast" for i in range(contrast_num)])} {changed_file}'
    exec_command(script)
    
    return changed_file

########################
# BioFormats Functions #
########################

def parse_meta_by_filename(image_file, filename):
    return False, None, None, None

def parse_meta_by_bioformats(image_file, series = 0):
    javabridge.start_vm(class_path=bioformats.JARS,run_headless=True,max_heap_size='16G')
    javabridge.attach()

    try:
        rdr = bioformats.ImageReader(image_file, perform_init=True)
        reader = rdr.rdr

        series_count = reader.getSeriesCount()
        image_count = reader.getImageCount()

        reader.setSeries(series)

        series = reader.getSeries()

        size_x = reader.getSizeX()
        size_y = reader.getSizeY()
        size_z = reader.getSizeZ()
        size_t = reader.getSizeT()
        size_c = reader.getSizeC()
        rgb_channel_count = reader.getRGBChannelCount()
        dimension_order = reader.getDimensionOrder()
        is_rgb = reader.isRGB()
        is_little_endian = reader.isLittleEndian()
        is_interleaved = reader.isInterleaved()
        pixel_type = reader.getPixelType()

        print("Number of series per file === %d" %                          series_count)
        print("Total number of images per series === %d" %                  image_count)
        print("Image width === %d" %                                        size_x)
        print("Image height === %d" %                                       size_y)
        print("Actual number of channels in the current series === %d" %    size_c)
        print("Number of slices in the current series === %d" %             size_z)
        print("Number of time points in the current series === %d" %        size_t)
        print("Number of channels per image === %d" %                       rgb_channel_count)
        print("Order of images in the current series === %s" %              dimension_order)
        print("Whether each image is RGB === %r" %                          is_rgb)
        print("Whether pixel bytes are in little-endian order === %r" %     is_little_endian)
        print("Whether the image channel is interleaved === %r" %           is_interleaved)
        print("The type of pixel data in this file === %d" %                pixel_type)

        meta={'SeriesCount': series_count}
        meta['ImageCount'] = image_count

        meta['CurrentSeries'] = series
        meta['SizeX'] = size_x
        meta['SizeY'] = size_y
        meta['SizeC'] = size_c
        meta['SizeZ'] = size_z
        meta['SizeT'] = size_t
        meta['RGBChannelCount'] = rgb_channel_count
        meta['DimensionOrder'] = dimension_order
        meta['IsRGB'] = is_rgb
        meta['IsLittleEndian'] = is_little_endian
        meta['IsInterleaved'] = is_interleaved
        meta['PixelType'] = pixel_type
        ### PixelType ###
        # FormatTools.INT8 - 0
        # FormatTools.UINT8 - 1
        # FormatTools.INT16 - 2
        # FormatTools.UINT16 - 3
        # FormatTools.INT32 - 4
        # FormatTools.UINT32 - 5
        # FormatTools.FLOAT - 6 
        # FormatTools.DOUBLE - 7

        image00, scale00 = rdr.read(z=0, t=0, series=series, rescale=False, wants_max_intensity=True)
        sy = len(image00)
        sx = len(image00[0])

        if type(image00[0, 0]) is np.ndarray:
            size = (size_t, size_z, sy, sx, len(image00[0, 0]))
        else:
            size = (size_t, size_z, sy, sx)

        print(size)

        image5d0 = np.zeros(size)
        scale = np.zeros((size_t, size_z))
        for t in range(size_t):
            for z in range(size_z):
                if t == 0 and z == 0:
                    image5d0[t, z] = image00
                    scale[t, z] = scale00
                else:
                    image5d0[t, z], scale[t, z] = rdr.read(z=z, t=t, series=series, rescale=False, wants_max_intensity=True)

        reader.close()

        javabridge.kill_vm()

        return True, meta, image5d0, scale
    except Exception:
        javabridge.kill_vm()

        print_exc()
        print('========= ERROR =========')
        return False, None, None, None
        
    
