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
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class GaussianBlur(Filter):

    """Smoothes an image using a Gaussian filter"""

    def __init__(self):
        Filter.__init__(self)
        self.kernel_height = Param("Kernel Height", 3, min_v=1, max_v=256)
        self.kernel_width = Param("Kernel Width", 3, min_v=1, max_v=256)
        self.sigma_x = Param("Sigma X", 3, min_v=1, max_v=256)
        self.sigma_y = Param("Sigma Y", 3, min_v=1, max_v=256)

    def execute(self, image):
        cv2.GaussianBlur(image,
                         (self.kernel_height.get(),
                          self.kernel_width.get()),
                         sigmaX=self.sigma_x.get(),
                         sigmaY=self.sigma_y.get(),
                         dst=image)
        return image
