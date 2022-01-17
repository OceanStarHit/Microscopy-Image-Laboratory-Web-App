import os
import glob
import numpy as np
from numpy.core.fromnumeric import shape
from scipy import ndimage

from mainApi.app.images.utils.flowdec import data as fd_data
from mainApi.app.images.utils.flowdec import restoration as fd_restoration

import os
import cv2


def normalize_2Dim_uint8(im):
    im = im.astype(np.float32)
    min = np.min(im)
    max = np.max(im)
    im = (im-min)/(max-min)*255
    return im.astype(np.uint8)


def remove_png_files(dir):
    files = glob.glob(str(dir) + '/*.png')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def Deconvolve(raw_image, sigma = 1.):
    raw_image = raw_image.astype(np.float)
    # Create a gaussian kernel that will be used to blur the original acquisition:
    kernel = np.zeros_like(raw_image)
    for offset in [0, 1]:
        kernel[tuple((np.array(kernel.shape) - offset) // 2)] = 1
    kernel = ndimage.gaussian_filter(kernel, sigma=sigma)
    # kernel.shap

    # Run the deconvolution/algorithm (for 30 iterations):
    algo = fd_restoration.RichardsonLucyDeconvolver(raw_image.ndim).initialize()
    processed_2D_image = algo.run(fd_data.Acquisition(data=raw_image, kernel=kernel), niter=30).data

    return processed_2D_image 


# from focus_stack import focus_stacking as fs
from mainApi.app.images.utils.focus_stack import FocusStack

def Focus_Stack(raw_3D_image_array, laplacian_kernel_size=5, gaussian_blur_kernel_size=5):
    
    # stacker = fs.FocusStacker(laplacian_kernel_size=laplacian_kernel_size, gaussian_blur_kernel_size=gaussian_blur_kernel_size)
    # focus_stacked = stacker.focus_stack(raw_3D_image)
    images = []
    image = np.zeros((raw_3D_image_array.shape[1], raw_3D_image_array.shape[2], 3))
    for i in range(raw_3D_image_array.shape[0]):
        image[:,:,0] = image[:,:,1] = image[:,:,2] = normalize_2Dim_uint8(raw_3D_image_array[i])
        print(image.shape)
        images.append(image)
    
    focus_stacked = FocusStack.focus_stack(images, laplacian_kernel_size=laplacian_kernel_size, gaussian_blur_kernel_size=gaussian_blur_kernel_size)


    return focus_stacked
