#! /usr/bin/env python
#
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

# These are necessary for the executed code.
import cv2 #@UnusedImport
import cv2.cv as cv #@UnusedImport
import numpy as np #@UnusedImport

class Exec:
    """Create and edit a filter on the fly for testing purposes"""
    
    def __init__(self):
        self.code = ""
        self._ccode = None
        
    def set_code(self, code):
        self.code = code
        self._ccode = compile(code, '<string>', 'exec')
        
    def configure(self):
        self.set_code(self.code)
        
    def execute(self, image):
        try:
            if self._ccode is not None:
                exec self._ccode
        except Exception, e:
            print e
        return image
