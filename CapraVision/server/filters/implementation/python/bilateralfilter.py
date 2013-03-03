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

class BilateralFilter:
    """Applies the bilateral filter to an image."""
    
    def __init__(self):
        self.diameter = Parameter("Diameter", 0, 255, 10) 
        self.sigma_color = Parameter("Sigma Color", 0, 255, 20)
        self.sigma_space = Parameter("Sigma Space", 0, 255, 5)
        
    def execute(self, image):
        return cv2.bilateralFilter(image,
                            int(self.diameter.get_current_value()),
                            int(self.sigma_color.get_current_value()),
                            int(self.sigma_space.get_current_value()))
    
    