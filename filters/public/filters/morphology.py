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
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class Morphology(Filter):

    def __init__(self):
        Filter.__init__(self)
        self.kernel_width = Param("Kernel Width", 3, min_v=1, max_v=256)
        self.kernel_height = Param("Kernel Height", 3, min_v=1, max_v=256)
        self.anchor_x = Param("Anchor X", -1)
        self.anchor_y = Param("Anchor Y", -1)
        self.iterations = Param("Iteration,", 1, min_v=1)
        self.configure()

    def configure(self):
        self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                 (self.kernel_width.get(),
                                                  self.kernel_height.get()),
                                                 (self.anchor_x.get(),
                                                  self.anchor_y.get()))

    def execute(self, image):
        morph = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cv2.morphologyEx(
            morph,
            cv2.MORPH_CLOSE,
            self._kernel,
            dst=morph,
            iterations=self.iterations.get())
        cv2.merge((morph, morph, morph), image)

        return image
