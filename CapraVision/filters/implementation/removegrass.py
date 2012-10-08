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

class RemoveGrass:
    
    def __init__(self):
        self.threshold = 330
    
    def execute(self):
        image = cv2.blur(image, (3,3))
        blue, green, red = cv2.split(image.astype('uint16'))
        threshold = (green + blue) > 330
        image[:,:,0] = blue * threshold
        image[:,:,1] = green * threshold
        image[:,:,2] = red * threshold
        return image