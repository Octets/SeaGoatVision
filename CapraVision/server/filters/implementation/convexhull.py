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

from CapraVision.server.filters import dataextract
from CapraVision.server.filters.parameter import  Parameter

class ConvexHull(dataextract.DataExtractor):
        
    def __init__(self):
        dataextract.DataExtractor.__init__(self)
        self.area_min = Parameter("Area Min", 1, 100000, 300)
        self.area_max = Parameter("Area Max", 1, 100000, 35000)
    
    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cnt, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image *= 0
        for c in cnt:
            hull = cv2.convexHull(c)
            approx = cv2.approxPolyDP(c, 0, False)
            area = np.abs(cv2.contourArea(c))
            
            if self.area_min.get_current_value() < area:
                cv2.drawContours(image, [hull],-1, (255,255,255), -1)
                #self.notify_output_observers(str(area) + "\n")
                
        return image
    