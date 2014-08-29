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
import math
import numpy as np

from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class LineOrientation(Filter):
    """Port of the old line detection code"""

    def __init__(self):
        Filter.__init__(self)
        self.area_min = Param("Area Min", 300, min_v=1, max_v=100000)
        self.area_max = Param("Area Max", 35000, min_v=1, max_v=100000)

        self._kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (3, 3), (0, 0))

    def execute(self, image):
        image_threshold = cv2.split(image)[0]
        image_morphology = cv2.morphologyEx(
            image_threshold, cv2.MORPH_CLOSE, self._kernel, iterations=1)

        contours, _ = cv2.findContours(
            image_morphology,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE)
        lines = self.find_lines(contours, image)
        self.draw_lines(lines, image)

        return image

    def draw_lines(self, lines, image):
        msg = "LineOrientation: x1=%s x2=%s y1=%s y2=%s \n"
        for l, t in lines:
            vx, vy, x, y = l
            point1 = (x - t * vx, y - t * vy)
            point2 = (x + t * vx, y + t * vy)
            to_send = msg % (int(point1[0][0]),
                             int(point1[1][0]),
                             int(point2[0][0]),
                             int(point2[1][0]))
            self.notify_output_observers(to_send)
            cv2.line(image, point1, point2, (0, 0, 255), 3, -1)
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        self.notify_output_observers("LineOrientation: \n")

    def find_lines(self, contours, image):
        lines = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0, False)
            area = np.abs(cv2.contourArea(contour))

            if self.area_min.get() < area < self.area_max.get():
                line_values = cv2.fitLine(approx, cv.CV_DIST_L2, 0, 0.01, 0.01)
                rect = cv2.boundingRect(approx)
                t = math.sqrt((rect[2] ** 2 + rect[3] ** 2) / 2.0)
                lines.append((line_values, t))
                cv2.drawContours(image, contour, -1, (255, 255, 0))

        return lines
