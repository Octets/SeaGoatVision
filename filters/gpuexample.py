#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# http://opencv.willowgarage.com/wiki/OpenCV_GPU

# Mapping between Numpy and C++
# image.shape = Nimage
# image.strides = Simage
# image.ndim = Dimage
# image.data = image

import scipy.weave as weave
from SeaGoatVision.server.core.filter import Filter

class GPUExample(Filter):
    """Example on how to use scipy.weave to access the GPU with OpenCV.
        http://opencv.willowgarage.com/wiki/OpenCV_GPU"""

    def __init__(self):
        Filter.__init__(self)

    def execute(self, image):
        """
        Mapping between Numpy and C++
        image.shape = Nimage
        image.strides = Simage
        image.ndim = Dimage
        image.data = image"""

        weave.inline(
        """
        // Convert numpy array to C++ Mat object
        // The image data is accessed directly, there is no copy
        cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);

        // The matrix must be uploaded to the gpu before processing
        // This is essential to avoid too much data transfer between cpu and gpu
        cv::gpu::GpuMat gpuimg;
        gpuimg.upload(mat);

        // Process image here
        cv::gpu::cvtColor(gpuimg, gpuimg, CV_BGR2HSV);

        // Download result in original matrix
        // The numpy image is modified here.  No further steps are required
        gpuimg.download(mat);
        """,
        arg_names=['image'],
        headers=['<opencv2/opencv.hpp>', '<opencv2/gpu/gpu.hpp>'],
        extra_objects=["`pkg-config --cflags --libs opencv`"])

        return image
