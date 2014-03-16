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

import cv2
from cv2 import cv
import numpy as np
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class Canny(Filter):

    """Apply a canny filter to the image"""

    def __init__(self):
        Filter.__init__(self)
        self.threshold1 = Param("Threshold1", 10, min_v=0, max_v=255)
        self.threshold2 = Param("Threshold2", 100, min_v=0, max_v=255)

    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)

        cv2.Canny(gray,
                  self.threshold1.get(),
                  self.threshold2.get(),
                  gray)
        cv2.merge((gray, gray, gray), image)

        return image
