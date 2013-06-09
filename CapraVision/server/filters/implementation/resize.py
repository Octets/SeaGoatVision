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
import math
import numpy as np
from CapraVision.server.filters.parameter import  Parameter

class Resize():
    """Resizes an image"""
    
    def __init__(self):
        self.width = Parameter("Width",100,2584,1292)
        self.height = Parameter("Height",100,1468,734)

    def configure(self):
        pass

    def execute(self, image): 
        width = int(self.width.get_current_value())
        height = int(self.height.get_current_value())
        image = cv2.resize(image,(width,height))
        return image
    