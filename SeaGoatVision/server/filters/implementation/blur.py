#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#    
#    SeaGoatVision is free software: you can redistribute it and/or modify
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
from SeaGoatVision.server.filters.param import Param
from SeaGoatVision.server.core.filter import Filter

class Blur(Filter):
    """Smoothes an image using the normalized box filter"""
    def __init__(self):
        Filter.__init__(self)
        self.kernel_width = Param("width", 3, min_v=1, max_v=10)
        self.kernel_height = Param("height", 3, min_v=1, max_v=10)        
    
    def execute(self, image):
        cv2.blur(image, (self.kernel_width.get(), 
                        self.kernel_height.get()),
                        image)
        return image
    