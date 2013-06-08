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

class Split():
    
    def __init__(self):
        pass

    def execute(self, image):
        #f = open("cropconf", 'r')
        
        row = 2
        thickness = 3

        height, width, channels = image.shape
        
        for i in range(1, row):
            cv2.rectangle(image, (0, height/row * i - thickness), (width, height/row * i + thickness), (0, 0, 0), -1) 
        return image
    