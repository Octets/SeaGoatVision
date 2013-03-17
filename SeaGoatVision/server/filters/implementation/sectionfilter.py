#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
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

from SeaGoatVision.server.filters.param import  Param
from SeaGoatVision.server.core.filter import Filter

class SectionFilter(Filter):
    """"""

    def __init__(self):
        Filter.__init__(self)
        self.kernel_erode_height = Param("Kernel Erode Height", 3, min_v=1, max_v=255)
        self.kernel_erode_width = Param("Kernel Dilate Width", 3, min_v=1, max_v=255)
        self.kernel_dilate_height = Param("Kernel Erode Height", 5, min_v=1, max_v=255)
        self.kernel_dilate_width = Param("Kernel Dilate Width", 5, min_v=1, max_v=255)
        self.sections = Param("Sections", 5, min_v=1, max_v=10)
        self.min_area = Param("Minimum Area", 1000, min_v=1, max_v=65535)
        self.configure()

    def configure(self):
        self.kerode = cv2.getStructuringElement(
                         cv2.MORPH_CROSS,
                         (self.kernel_erode_width.get(),
                          self.kernel_erode_height.get()))
        self.kdilate = cv2.getStructuringElement(
                         cv2.MORPH_CROSS,
                         (iself.kernel_dilate_width.get(),
                          self.kernel_dilate_height.get()))

    def execute(self, image):

        image = cv2.erode(image, self.kerode)

        rows = image.shape[0]
        section_size = rows / self.sections.get()
        for i in xrange(0, self.sections.get()):
            start = (section_size) * i
            end = (section_size) * (i + 1)
            if end > rows:
                end = rows
            section = image[start : end]

            gray = cv2.split(section)[0]
            contours, _ = cv2.findContours(
                                       gray,
                                       cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

            section = np.zeros(section.shape, np.uint8)
            for contour in contours:
                area = np.abs(cv2.contourArea(contour))
                if area > self.min_area.get():
                    cv2.drawContours(section,
                                 [cv2.convexHull(contour)],
                                 - 1,
                                 (255, 255, 255),
                                 thickness= -1)
            image[start: end] = section


        image = cv2.dilate(image, self.kdilate)

        return image

