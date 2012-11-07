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

from CapraVision.server.filters.filter import Filter

class ColorLeve(Filter):
    """Determine the value in % a color will have.
        0% = Nothing
        50% = Half the original value.
        100% = Original
        Example: With 50% Blue and the following pixel (100, 100, 100) give (50, 100, 100)"""
    def __init__(self):
        Filter.__init__(self)
        self.red = 100
        self.green = 100
        self.blue = 100
        
    def execute(self, image):
        if self.red <> 100:
            image[:,:, 2] *= (self.red/100)
        #image[:,:, 1] *= ((image[:,:, 0])/2)
        if self.green <> 100:
            image[:,:, 1] *= (self.green/100)
        if self.blue <> 100:
            image[:,:, 0] *= (self.blue/100) 
        return image
