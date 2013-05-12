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
import cv2.cv as cv
import numpy as np
from CapraVision.server.filters.parameter import  Parameter

class HSVEnhancer:
    """
    """
    def __init__(self):
        self.color_mult = Parameter("Color Multiplier", 1, 255, 2)
        self.value_min_h = Parameter("Value Min H", 1, 255, 20)
        self.value_max_h = Parameter("Value Max H", 1, 255, 255)
        self.value_min_s = Parameter("Value Min S", 1, 255, 1)
        self.value_max_s = Parameter("Value Max S", 1, 255, 255)
        self.value_min_v = Parameter("Value Min V", 1, 255, 1)
        self.value_max_v = Parameter("Value Max V", 1, 255, 255)
            
    def execute(self, image):
        hsv = cv2.cvtColor(image, cv2.cv.CV_BGR2HSV)
        r, g, b = cv2.split(image)
        h, s, v = cv2.split(hsv)
        r = r.astype(np.int16)
        g = g.astype(np.int16)
        b = b.astype(np.int16)
        h = h.astype(np.int16)
        s = s.astype(np.int16)
        v = v.astype(np.int16)
        c = 255 - r
        m = 255 - g
        y = 255 - b
        k = np.minimum(np.minimum(c, m), y)
        ychan = (y - k) * self.color_mult.get_current_value() / (255 - k)
        newcolor = s * ychan
        colorout = np.zeros(ychan.shape, np.int16)
        if self.value_max_h.get_current_value > self.value_min_h:
            mask = ((h >= self.value_min_h.get_current_value()) & 
                      (h <= self.value_max_h.get_current_value()))
            colorout[mask] = newcolor[mask]
        else:
            mask = (((h >= self.value_min_h.get_current_value()) & 
                      (h <= self.value_max_h.get_current_value()))
                      (s >= self.value_min_s.get_current_value()) & 
                      (s <= self.value_max_s.get_current_value()) & 
                      (v >= self.value_min_v.get_current_value()) & 
                      (v <= self.value_max_v.get_current_value()))
            colorout[mask] = newcolor[mask]
            
        colorout[colorout < 0] = 0
        colorout[colorout > 255] = 255
        colorout = colorout.astype(np.uint8)
        return cv2.merge((colorout, colorout, colorout))
    