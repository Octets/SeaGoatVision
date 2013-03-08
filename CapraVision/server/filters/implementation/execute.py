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
import sys

import scipy.weave as weave

class Exec:
    """Create and edit a filter on the fly for testing purposes"""
    
    def __init__(self):
        self.code = ""
        self.is_python = True
        self._ccode = None
        self._has_error = False
        
    def set_code(self, code, is_python):
        self._has_error = False
        self.is_python = is_python
        try:
            self.code = code
            if self.is_python:
                self._ccode = compile(code, '<string>', 'exec')
        except Exception,e:
            sys.stderr.write(str(e) + '\n')
            self._has_error = True
            
    def exec_python(self, image):
        if self._ccode is not None:
            exec self._ccode
        return image
    
    def exec_cpp(self, numpy_array):
        weave.inline(
        """
        // Convert numpy array to C++ Mat object
        // The image data is accessed directly, there is no copy
        cv::Mat image(Nnumpy_array[0], Nnumpy_array[1], CV_8UC(3), numpy_array);
        """ + self.code,
        arg_names = ['numpy_array'],
        headers = ['<opencv2/opencv.hpp>', '<opencv2/gpu/gpu.hpp>'],
        extra_objects = ["`pkg-config --cflags --libs opencv`"])

        return numpy_array
    
    def configure(self):
        self._has_error = False
        self.set_code(self.code, self.is_python)
        
    def execute(self, image):
        if self._has_error:
            return image
        try:
            if self.is_python:
                image = self.exec_python(image)
            else:
                image = self.exec_cpp(image)
        except Exception, e:
            sys.stderr.write(str(e) + '\n')
            self._has_error = True
        return image
