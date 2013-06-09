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

import cv,cv2
import numpy

class Undistort:
    """Do nothing"""
    
    def execute(self, image):
    
        distCoeffs = numpy.array([-0.34, 0.085, 0, 0, -0.007])
        cameraMatrix = numpy.matrix([[630.79035702238025/2.0, 0, 645.50000000000000/2.0],
                                     [0, 630.79035702238025/2.0, 366.50000000000000/2.0],
                                     [0,                  0,                  1]])
        size = (1292/2, 734/2)
        
        #technique 2
        newimage = numpy.matrix([])
        largeCameraMatrix = numpy.matrix([[630.79035702238025, 0, 645.50000000000000],
                                          [0, 630.79035702238025, 366.50000000000000],
                                          [0,                  0,                  1]])
        optimalMat, roi = cv2.getOptimalNewCameraMatrix(largeCameraMatrix, distCoeffs, size, 1)
        
        #The last parameter may be optimalMat if we want to keep all the original image.
        #It will add a black zone where the distortion has impacted the image.
        newimage = cv2.undistort(image, cameraMatrix, distCoeffs, newimage, cameraMatrix)
        
        return newimage