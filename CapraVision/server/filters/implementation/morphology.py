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

class Morphology:
    
    def __init__(self):
        self.kernel_width = 3
        self.kernel_height = 3
        self.anchor_x = -1
        self.anchor_y = -1
        self.iterations = 1
        self.configure()
        
    def configure(self):
        self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                                (self.kernel_width, 
                                                 self.kernel_height), 
                                                (self.anchor_x, 
                                                 self.anchor_y))
    
    def execute(self, image):
        image_threshold = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        image_morphology = cv2.morphologyEx(
                image_threshold, cv2.MORPH_CLOSE, self._kernel, iterations=1)
        image[:, :, 0] = image_morphology
        image[:, :, 1] = image_morphology
        image[:, :, 2] = image_morphology
        
        return image