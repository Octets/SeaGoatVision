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


class ExePy1(Filter):
    """
    Python Example Test #1
    Convert BGR color to another color.
    """

    def __init__(self):
        Filter.__init__(self)

        self.convert_color = Param("Convert choice", 1, min_v=0, max_v=4)
        desc = "0 = original\n1 = BGR TO YUV\n2 = BGR TO HSV\n3 = BGR TO RGB\n\
        4 = BGR TO GRAY"
        self.convert_color.set_description(desc)

    def execute(self, image):
        convert_color = self.convert_color.get()

        if convert_color == 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        elif convert_color == 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif convert_color == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif convert_color == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
