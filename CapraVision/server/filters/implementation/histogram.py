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

class Histogram:
    
    def execute(self, image):
        hsv = cv2.cvtColor(image, cv.CV_BGR2HSV)
        h,s,v = cv2.split(hsv)
        
        #hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0,256])
        #cv.ThreshHist(hist, 200)
        
        dst = cv2.equalizeHist(s)
        return hist
