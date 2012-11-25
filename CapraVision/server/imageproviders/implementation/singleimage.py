#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of CapraVision.
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

class SingleImage:
    
    def __init__(self):
        self.file = ''
        self.image = None
        
    def __iter__(self):
        return self
    
    def set_image(self, filename):
        self.file = filename
        self.image = cv2.imread(self.file)
        
    def next(self):
        if self.image is None:
            return None
        else:
            return self.image.copy()
    
    def close(self):
        pass
    
    