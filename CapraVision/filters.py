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

'''
Created on 2012-07-28

@author: Benoit Paquet
'''

import cv2.cv as cv, cv2
import numpy as np

def noop(image):
    return image

def bgr_to_rgb(image):
    image = cv2.cvtColor(image, cv.CV_BGR2RGB)
    return image

def bgr_to_hsv(image):
    image = cv2.cvtColor(image, cv.CV_BGR2HSV)
    #image = cv2.cvtColor(image, cv.CV_BGR2GRAY)
    return image
    
def bgr_to_grayscale(image):
    image = cv2.cvtColor(image, cv.CV_BGR2GRAY)
    return image

def bgr_to_yuv(image):
    image = cv2.cvtColor(image, cv.CV_BGR2YCrCb)
    return image

def yuv_to_bgr(image):
    image = cv2.cvtColor(image, cv.CV_YCrCb2BGR)
    return image
    
class RGBLevel():
    
    def __init__(self):
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

class RGBThreshold:
    
    def __init__(self):
        self.shift_hue_plane = False
        self.bluemin = 20.0
        self.bluemax = 256.0
        self.greenmin = 20.0
        self.greenmax = 256.0
        self.redmin = 20.0
        self.redmax = 256.0
        self.barray = None
        self.garray = None
        self.rarray = None
        self.configure()
    
    def configure(self):
        self.barray = np.array([self.get_binary_value(self.bluemin, self.bluemax, x) for x in range(0, 256)], dtype=np.float32)
        self.garray = np.array([self.get_binary_value(self.greenmin, self.greenmax, x) for x in range(0, 256)], dtype=np.float32)
        self.rarray = np.array([self.get_binary_value(self.redmin, self.redmax, x) for x in range(0, 256)], dtype=np.float32)
        
    def execute(self, image):
        image[:,:, 0] = image[:,:, 1] = image[:,:, 2] = 255 * self.barray[image[:,:, 0]] * self.garray[image[:,:, 1]] * self.rarray[image[:,:, 2]]
        return image

    def get_binary_value(self, mini, maxi, val):
        if mini <= val <= maxi:
            return 1.0
        else:
            return 0.0

class Perspective:
    
    def __init__(self):
        self.topleftx = 0
        self.toplefty = 0
        self.bottomleftx = 100
        self.bottomlefty = 480
        self.toprightx = 640
        self.toprighty = 0
        self.bottomrightx = 540
        self.bottomrighty = 480
        
        self.mmat = None
        self.configure()
        
    def configure(self):
        c1 = np.array([[self.topleftx, self.toplefty], [self.bottomleftx, self.bottomlefty], [self.toprightx, self.toprighty], [self.bottomrightx, self.bottomrighty]], np.float32)
        c2 = np.array([[0, 0], [0, 480], [640, 0], [640, 480]], np.float32)
        self.mmat = cv2.getPerspectiveTransform(c2, c1)
        
    def execute(self, image):
        return cv2.warpPerspective(image, self.mmat, (640, 480))
