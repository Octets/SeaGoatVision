#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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

import cv
import cv2
import numpy
from SeaGoatVision.server.core.filter import Filter


class Undistort(Filter):

    """Do nothing"""

    def __init__(self):
        Filter.__init__(self)

    def execute(self, image):

        dist_coeffs = numpy.array([-0.34, 0.085, 0, 0, -0.007])
        camera_matrix = numpy.matrix(
            [[630.79035702238025, 0, 645.50000000000000], [0, 630.79035702238025, 366.50000000000000], [0, 0, 1]])
        size = (1292, 734)

        # technique 2
        newimage = numpy.matrix([])
        optimal_mat, roi = cv2.getOptimalNewCameraMatrix(
            camera_matrix, dist_coeffs, size, 1)
        newimage = cv2.undistort(
            image,
            camera_matrix,
            dist_coeffs,
            newimage,
            optimal_mat)

        return newimage
