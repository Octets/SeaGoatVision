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

from CapraVision.server.filters.parameter import  Parameter

class MarioBros3FinalWorldView:
    """Only show a part of the image inside an ellipse"""
    
    def __init__(self):
        self._shape = None
        self.center_x = 100
        self.center_y = 100
        self.size_x = 50
        self.size_y = 50
        
    def configure(self):
        print 'congih'
        self._mask = np.zeros(self._shape, np.uint8)
        cv2.ellipse(self._mask, (self.center_x, self.center_y), 
                    (self.size_x, self.size_y), 
                    0, 0, 360, (255,255,255), -1)
        
    def execute(self, image):
        if self._shape == None:
            self._shape = image.shape
            self.configure()
        else:
            self._shape = image.shape
            
        image[self._mask == 0] *= 0
        return image