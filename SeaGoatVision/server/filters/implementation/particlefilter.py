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
import numpy as np
from SeaGoatVision.server.filters.parameter import  Parameter
from SeaGoatVision.server.core.filter import Filter

class ParticleFilter(Filter):
    """Remove small particles from the image.
        The image is first converted to grayscale and is then eroded and 
        the remaining blobs are filtered according to the area of the blobs."""
    
    def __init__(self):
        Filter.__init__(self)
        self.kernel_height = Parameter("Kernel Height",1,256,10)
        self.kernel_width = Parameter("Kernel Width",1,256,10)
        self.area_min = Parameter("Area Min",1,None,3200)
        self.configure()
        
    def configure(self):
        self._kernel = cv2.getStructuringElement(
                                                 cv2.MORPH_CROSS, 
                                                 (int(self.kernel_width.get_current_value()), 
                                                  int(self.kernel_height.get_current_value())))
            
    def execute(self, image):
        cv2.erode(image, self._kernel, image)
        gray = cv2.split(image)[0]
        contours, _ = cv2.findContours(
                                       gray, 
                                       cv2.RETR_TREE, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        image = np.zeros(image.shape, np.uint8)
        for contour in contours:
            area = np.abs(cv2.contourArea(contour))
            if area > self.area_min.get_current_value():
                cv2.drawContours(image, 
                                 [contour], 
                                 -1, 
                                 (255, 255, 255), 
                                 thickness=-1)        
        return image
    