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

from CapraVision.filters.filter import Filter

class Perspective(Filter):
    """Wrap perspective"""
    def __init__(self):
        Filter.__init__(self)
        self.topleftx = 0
        self.toplefty = 0
        self.bottomleftx = 100
        self.bottomlefty = 480
        self.toprightx = 640
        self.toprighty = 0
        self.bottomrightx = 540
        self.bottomrighty = 480
        
        self.mmat = None
        self.configure()
        
    def configure(self):
        c1 = np.array([[self.topleftx, self.toplefty], 
                       [self.bottomleftx, self.bottomlefty], 
                       [self.toprightx, self.toprighty], 
                       [self.bottomrightx, self.bottomrighty]], 
                      np.float32)
        c2 = np.array([[0, 0], [0, 480], [640, 0], [640, 480]], np.float32)
        self.mmat = cv2.getPerspectiveTransform(c2, c1)
        
    def execute(self, image):
        return cv2.warpPerspective(image, self.mmat, (640, 480))
