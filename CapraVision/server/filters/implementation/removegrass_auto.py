#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of CapraVision.
#    
#    CapraVision is free software: you can redistribute it and/or modify
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

class RemoveGrassAuto:
    """"""
    
    def __init__(self):
        pass
    
    def execute(self, image):
        #copy = cv2.cvtColor(image, cv2.cv.CV_BGR2HSV)
        h, s, v = cv2.split(image)
        image[(h > 12) & (h < 80)] = 0
        return image
    
        blue, green, red = cv2.split(image)
        new_blue = np.subtract(blue, green / 2)
        black = blue < new_blue
        new_blue[black] = 0
        avg = np.average(green / 2)
        threshold = new_blue < avg
        blue[threshold] = 0
        green[threshold] = 0
        red[threshold] = 0
        image = cv2.merge((blue, green, red))

        return image
    