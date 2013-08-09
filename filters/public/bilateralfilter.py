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

from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter

class BilateralFilter(Filter):
    """Applies the bilateral filter to an image."""

    def __init__(self):
        Filter.__init__(self)
        self.diameter = Param("Diameter", 10, min_v=0, max_v=255)
        self.sigma_color = Param("Sigma Color", 0, min_v=0, max_v=255)
        self.sigma_space = Param("Sigma Space", 0, min_v=0, max_v=255)

    def execute(self, image):
        return cv2.bilateralFilter(image,
                            self.diameter.get(),
                            self.sigma_color.get(),
                            self.sigma_space.get())

