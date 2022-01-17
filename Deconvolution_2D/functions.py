import os
import glob
import numpy as np
from numpy.core.fromnumeric import shape
from scipy import ndimage

from mainApi.app.images.utils.flowdec import data as fd_data
from mainApi.app.images.utils.flowdec import restoration as fd_restoration

import os
import cv2

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

