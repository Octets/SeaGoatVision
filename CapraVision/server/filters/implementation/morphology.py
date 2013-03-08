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
from CapraVision.server.filters.parameter import  Parameter

class Morphology:
    
    def __init__(self):
        self.kernel_width = Parameter("Kernel Width",1,256,3)
        self.kernel_height = Parameter("Kernel Height",1,256,3)
        self.anchor_x = Parameter("Anchor X",None,None,-1)
        self.anchor_y = Parameter("Anchor Y",None,None,-1)
        self.iterations = Parameter("Iteration,",1,None,1)
        self.configure()
        
    def configure(self):
        self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                (int(self.kernel_width.get_current_value()), 
                                int(self.kernel_height.get_current_value())), 
                                (int(self.anchor_x.get_current_value()), 
                                int(self.anchor_y.get_current_value())))
    
    def execute(self, image):
        morph = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cv2.morphologyEx(
                morph, 
                cv2.MORPH_CLOSE, 
                self._kernel,
                dst=morph, 
                iterations=int(self.iterations.get_current_value()))
        cv2.merge((morph, morph, morph), image)
        
        return image