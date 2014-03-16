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

import numpy as np
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class ColorThreshold(Filter):

    """Apply a binary threshold on the three channels of the images
        Each channel have a minimum and a maximum value.
        Everything within this threshold is white (255, 255, 255)
        Everything else is black (0, 0, 0)"""

    def __init__(self):
        Filter.__init__(self)
        self.blue = Param("Blue", 20, min_v=1, max_v=256, thres_h=256)
        self.green = Param("Green", 20, min_v=1, max_v=256, thres_h=256)
        self.red = Param("Red", 20, min_v=1, max_v=256, thres_h=256)
        self._barray = None
        self._garray = None
        self._rarray = None
        self.configure()

    def configure(self):
        min_v, max_v = self.blue.get()
        self._barray = np.array([1.0 * (min_v <= x <= max_v)
                                 for x in range(0, 256)], dtype=np.float32)
        min_v, max_v = self.green.get()
        self._garray = np.array([1.0 * (min_v <= x <= max_v)
                                 for x in range(0, 256)], dtype=np.float32)
        min_v, max_v = self.red.get()
        self._rarray = np.array([1.0 * (min_v <= x <= max_v)
                                 for x in range(0, 256)], dtype=np.float32)

    def execute(self, image):
        image[:, :, 0] = image[:, :, 1] = image[:, :, 2] = (
            255 * self._barray[image[:, :, 0]] *
            self._garray[image[:, :, 1]] *
            self._rarray[image[:, :, 2]])
        return image
