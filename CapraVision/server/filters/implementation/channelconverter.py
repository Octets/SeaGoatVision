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

from CapraVision.server.filters.parameter import  Parameter

class ChannelConverter:
    
    def __init__(self):
        self.channels = Parameter("channels", 1, 3, 3)
        
    def execute(self, image):
        if image[0][0].size == 1 and self.channels.get_current_value() == 3 or \
        len(image.shape) == 2 and self.channels.get_current_value() == 3:
            return cv2.merge((image, image, image))            
        elif image[0][0].size == 3 and self.channels.get_current_value() == 1:
            return cv2.cvtColor(image, cv.CV_BGR2GRAY)
        else:
            return image
