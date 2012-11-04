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
import numpy as np

class RemoveGrass:
    """Remove grass from an image"""
    
    def __init__(self):
        self.threshold = 100
        self.technique = 0
        
    def remove_green_from_blue(self, image):
        blue, green, red = cv2.split(image)
        new_blue = blue - green / 2
        black = blue < new_blue
        new_blue[black] = 0
        threshold = new_blue < self.threshold
        blue[threshold] = 0
        green[threshold] = 0
        red[threshold] = 0
        image[:,:,0] = blue
        image[:,:,1] = green 
        image[:,:,2] = red 
        return image
    
    def add_green_to_blue(self, image):
        blue, green, red = cv2.split(image)
        new_color = green + blue
        white = ((new_color < green) & (new_color < blue))
        new_color[white] = 255
        threshold = new_color > self.threshold
        blue[threshold] = 0
        green[threshold] = 0
        red[threshold] = 0
        image[:,:,0] = blue
        image[:,:,1] = green
        image[:,:,2] = red
        return image
        
    def enhance_grass(self, image):
        blue, green, red = cv2.split(image)
        image[:,:,0] = np.subtract(blue, green / 2)
        return image
    
    def execute(self, image):
        if self.technique == 0:
            return self.add_green_to_blue(image)
        elif self.technique == 1:
            return self.remove_green_from_blue(image)
        elif self.technique == 2:
            return self.enhance_grass(image)
            