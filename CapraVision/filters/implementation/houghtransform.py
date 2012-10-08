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

class HoughTransform:
    
    def __init__(self):
        self.canny1 = 50
        self.canny2 = 200
        self.rho = 1
        self.theta = 180
        self.threshold = 100
        self.line_size = 1000
            
    def execute(self, image):
        edges = cv2.Canny(image, self.canny1, self.canny2)
        lines = cv2.HoughLines(edges, self.rho, cv.CV_PI / self.theta, self.threshold)
        if lines is None:
            return image
        rho = lines[:, :, 0]
        theta = lines[:, :, 1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        size = lines.shape[1]        
        pt1x = np.round(x0 + self.line_size * -b).astype(np.int)
        pt1y = np.round(y0 + self.line_size * a).astype(np.int)
        pt2x = np.round(x0 - self.line_size * -b).astype(np.int)
        pt2y = np.round(y0 - self.line_size * a).astype(np.int)
        
        for i in xrange(size):
            cv2.line(image, 
                     (pt1x.item(i), pt1y.item(i)), 
                     (pt2x.item(i), pt2y.item(i)), 
                     (0, 0, 255), 3, -1)
        return image
