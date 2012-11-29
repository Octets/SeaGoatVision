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
from CapraVision.server.filters.parameter import Parameter

class Blur:
    """Smoothes an image using the normalized box filter"""
    def __init__(self):
        
        self.kernel_width = Parameter("width",1,10,3)
        self.kernel_height = Parameter("height",1,10,3)
        self.parameters = [self.kernel_height,self.kernel_width]
    
    def execute(self, image):
        return cv2.blur(image, (int(self.kernel_width.get_current_value()), 
                                int(self.kernel_height.get_current_value())))
    