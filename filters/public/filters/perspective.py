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
import numpy as np
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class Perspective(Filter):

    """Wrap perspective"""

    def __init__(self):
        Filter.__init__(self)
        self.topleftx = Param("Top Left X", 0, min_v=0, max_v=640)
        self.toplefty = Param("Top Left TY", 0, min_v=0, max_v=480)
        self.bottomleftx = Param("Bottom Left X", 100, min_v=0, max_v=640)
        self.bottomlefty = Param("Bottom Left Y", 480, min_v=0, max_v=480)
        self.toprightx = Param("Top Right X", 640, min_v=0, max_v=640)
        self.toprighty = Param("Top Right Y", 0, min_v=0, max_v=480)
        self.bottomrightx = Param("Bottom Right X", 540, min_v=0, max_v=640)
        self.bottomrighty = Param("Bottom Right Y", 480, min_v=0, max_v=480)

        self.mmat = None
        self.configure()

    def configure(self):
        c1 = np.array([[self.topleftx.get(), self.toplefty.get()],
                       [self.bottomleftx.get(), self.bottomlefty.get()],
                       [self.toprightx.get(), self.toprighty.get()],
                       [self.bottomrightx.get(), self.bottomrighty.get()]],
                      np.float32)
        c2 = np.array([[0, 0], [0, 480], [640, 0], [640, 480]], np.float32)
        self.mmat = cv2.getPerspectiveTransform(c2, c1)

    def execute(self, image):
        cv2.warpPerspective(image, self.mmat, (640, 480), image)
        return image
