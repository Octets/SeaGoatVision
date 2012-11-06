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

from CapraVision.filters.filter import Filter

class ConvexHull(Filter):
    
    def __init__(self):
        Filter.__init__(self)
    
    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cnt, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnt:
            hull = cv2.convexHull(c)
            cv2.drawContours(image, [hull],-1, (255,255,255), -1)    
        return image