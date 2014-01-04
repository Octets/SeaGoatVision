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

import cv2
import cv2.cv as cv
import numpy as np
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class HoughTransform(Filter):

    """Apply a Canny filter to the image then
    finds lines in a binary image using the standard Hough transform"""

    def __init__(self):
        Filter.__init__(self)
        self.canny1 = Param("Canny1", 50, min_v=1, max_v=256)
        self.canny2 = Param("Canny2", 200, min_v=1, max_v=256)
        self.rho = Param("Rho", 1, min_v=1, max_v=256)
        self.theta = Param("Theta", 180, min_v=0, max_v=360)
        self.threshold = Param("Threshold", 100, min_v=1, max_v=256)
        self.line_size = Param("Line Size", 1000, min_v=1, max_v=2000)

    def execute(self, image):
        edges = cv2.Canny(image, self.canny1.get(), self.canny2.get())
        lines = cv2.HoughLines(
            edges,
            self.rho.get(),
            cv.CV_PI / self.theta.get(),
            self.threshold.get())
        if lines is None:
            return image
        rho = lines[:, :, 0]
        theta = lines[:, :, 1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        size = lines.shape[1]
        pt1x = np.round(x0 + self.line_size.get() * -b).astype(np.int)
        pt1y = np.round(y0 + self.line_size.get() * a).astype(np.int)
        pt2x = np.round(x0 - self.line_size.get() * -b).astype(np.int)
        pt2y = np.round(y0 - self.line_size.get() * a).astype(np.int)

        for i in xrange(size):
            cv2.line(image,
                     (pt1x.item(i), pt1y.item(i)),
                     (pt2x.item(i), pt2y.item(i)),
                     (0, 0, 255), 3, -1)
        return image
