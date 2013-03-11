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

from SeaGoatVision.server.filters.parameter import Parameter

class Rectangle:
    """Draw a black rectangle on top of the image"""
    
    def __init__(self):
        self.x1 = Parameter('x1', 0, 65535, 0)
        self.y1 = Parameter('y1', 0, 65535, 0)
        self.x2 = Parameter('x2', 0, 65535, 100)
        self.y2 = Parameter('y2', 0, 65535, 100)
    
    def execute(self, image):
        cv2.rectangle(image, 
            (int(self.x1.get_current_value()), int(self.y1.get_current_value())), 
            (int(self.x2.get_current_value()), int(self.y2.get_current_value())), 
            (0, 0, 0),
            cv2.cv.CV_FILLED)
        return image    
    