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
from CapraVision.server.filters.parameter import Parameter

class Canny:
    """Apply a canny filter to the image"""
    
    def __init__(self):
        self.threshold1 = Parameter("Threshold1",0,255,10)
        self.threshold2 = Parameter("Threshold2",0,255,100)
    
    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        
        cv2.Canny(gray, 
                  self.threshold1.get_current_value(), 
                  self.threshold2.get_current_value(),
                  gray)
        cv2.merge((gray, gray, gray), image)

        return image
    