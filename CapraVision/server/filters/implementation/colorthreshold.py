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

import numpy as np

from CapraVision.server.filters.filter import Filter

class ColorThreshold(Filter):
    """Apply a binary threshold on the three channels of the images
        Each channel have a minimum and a maximum value.
        Everything within this threshold is white (255, 255, 255)
        Everything else is black (0, 0, 0)"""
    def __init__(self):
        Filter.__init__(self)
        self.shift_hue_plane = False
        self.bluemin = 20.0
        self.bluemax = 256.0
        self.greenmin = 20.0
        self.greenmax = 256.0
        self.redmin = 20.0
        self.redmax = 256.0
        self._barray = None
        self._garray = None
        self._rarray = None
        self.configure()
    
    def configure(self):
        self._barray = np.array(
                        [self.get_binary_value(self.bluemin, self.bluemax, x) 
                            for x in range(0, 256)], dtype=np.float32)
        self._garray = np.array(
                        [self.get_binary_value(self.greenmin, self.greenmax, x) 
                            for x in range(0, 256)], dtype=np.float32)
        self._rarray = np.array(
                        [self.get_binary_value(self.redmin, self.redmax, x) 
                            for x in range(0, 256)], dtype=np.float32)
        
    def execute(self, image):
        image[:,:, 0] = image[:,:, 1] = image[:,:, 2] = (
                                            255 * self._barray[image[:,:, 0]] * 
                                            self._garray[image[:,:, 1]] * 
                                            self._rarray[image[:,:, 2]])
        return image

    def get_binary_value(self, mini, maxi, val):
        if mini <= val <= maxi:
            return 1.0
        else:
            return 0.0
