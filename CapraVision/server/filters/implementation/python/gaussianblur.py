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
from CapraVision.server.filters.parameter import  Parameter

class GaussianBlur:
    """Smoothes an image using a Gaussian filter"""
    def __init__(self):
        self.kernel_height = Parameter("Kernel Height",1,256,3)
        self.kernel_width = Parameter("Kernel Width",1,256,3)
        self.sigma_x = Parameter("Sigma X",1,256,3)
        self.sigma_y = Parameter("Sigma Y",1,256,3)
    
    def execute(self, image):
        return cv2.GaussianBlur(image, (self.kernel_height.get_current_value(), self.kernel_width.get_current_value()), 
                     sigmaX = self.sigma_x.get_current_value(), sigmaY = self.sigma_y.get_current_value())
        
    