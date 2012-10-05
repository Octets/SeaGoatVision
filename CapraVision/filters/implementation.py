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
""" Filters implementations
    Rules:
        - Filter must be a class
        - Filter must have a execute(image) function that 
            returns the processed image
        - Filter can have a configure() function to configure the 
            object after creation
        - If there are data members that must not be saved, the member name
            must start with an underscore.  
            Eg: self._dont_save = 123 # value will not be save
                self.save = 456 # value will be saved"""
import cv2.cv as cv, cv2
import numpy as np

class Noop:
    """Do nothing"""
    
    def execute(self, image):
        return image
    
class BGR2RGB:
    """Convert to RGB.  Useful for interacting with other libraries"""
    
    def execute(self, image):
        image = cv2.cvtColor(image, cv.CV_BGR2RGB)
        return image

class BGR2HSV:
    """Convert to Hue Saturation Brightness/Value"""
    
    def execute(self, image):
        image = cv2.cvtColor(image, cv.CV_BGR2HSV)
        return image
    
class BGR2Grayscale:
    """Convert to grayscale"""
    
    def execute(self, image):
        image = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        return image

class BGR2YUV:
    """Convert to YUV (Luminance with two colors)"""
    
    def execute(self, image):
        image = cv2.cvtColor(image, cv.CV_BGR2YCrCb)
        return image

class YUV2BGR:
    """Convert from YUV to BGR"""
    
    def execute(self, image):
        image = cv2.cvtColor(image, cv.CV_YCrCb2BGR)
        return image
            
class ColorLevel:
    """Determine the value in % a color will have.
        0% = Nothing
        50% = Half the original value.
        100% = Original
        Example: With 50% Blue and the following pixel (100, 100, 100) give (50, 100, 100)"""
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

class ColorThreshold:
    """Apply a binary threshold on the three channels of the images
        Each channel have a minimum and a maximum value.
        Everything within this threshold is white (255, 255, 255)
        Everything else is black (0, 0, 0)"""
    def __init__(self):
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

class Perspective:
    """Wrap perspective"""
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
        c1 = np.array([[self.topleftx, self.toplefty], 
                       [self.bottomleftx, self.bottomlefty], 
                       [self.toprightx, self.toprighty], 
                       [self.bottomrightx, self.bottomrighty]], 
                      np.float32)
        c2 = np.array([[0, 0], [0, 480], [640, 0], [640, 480]], np.float32)
        self.mmat = cv2.getPerspectiveTransform(c2, c1)
        
    def execute(self, image):
        return cv2.warpPerspective(image, self.mmat, (640, 480))

class Exec:
    """Create and edit a filter on the fly for testing purposes"""
    
    def __init__(self):
        self.code = ""
        
    def execute(self, image):
        try:
            if self.code.strip() <> "":
                exec self.code
        except Exception, e:
            print e
        return image
    
class HoughTransform:
    
    def __init__(self):
        pass
    
    def execute(self, image):
        edges = cv2.Canny(image, 50, 200)
        lines = cv2.HoughLines(edges, 1, cv.CV_PI / 180, 1)
        rho = lines[:, :, 0]
        theta = lines[:, :, 1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        size = lines.shape[1]        
        pt1x = np.round(x0 + 1000 * -b).astype(np.int)
        pt1y = np.round(y0 + 1000 * a).astype(np.int)
        pt2x = np.round(x0 - 1000 * -b).astype(np.int)
        pt2y = np.round(y0 - 1000 * a).astype(np.int)
        
        for i in xrange(size):
            cv2.line(image, 
                     (pt1x.item(i), pt1y.item(i)), 
                     (pt2x.item(i), pt2y.item(i)), 
                     (0, 0, 255))
        return image
    
class LineOrientation:
    """Port of the old line detection code"""
    
    def __init__(self):

        self.area_min = 300
        self.area_max = 35000
    
        self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                
    def execute(self, image):
        image_threshold = cv2.split(image)[0]
        image_morphology = cv2.morphologyEx(
                    image_threshold, cv2.MORPH_CLOSE, self._kernel)
                
        contours, hierarchy = cv2.findContours(
                                            image_morphology, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE)
        lines = self.find_lines(contours, image)
        self.draw_lines(lines, image)
        
        return image
    
    def draw_lines(self, lines, image):
        for l, t in lines:
            vx, vy, x, y = l
            point1 = (x - t * vx, y - t * vy)
            point2 = (x + t * vx, y + t * vy)
            cv2.line(image, point1, point2, (0, 0, 255), 3, -1)
            cv2.circle(image, (x, y), 5, (0, 255, 0))
            
    def find_lines(self, contours, image):
        lines = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 
                                      cv2.arcLength(contour, False), False)
            area = np.abs(cv2.contourArea(contour))
            
            if self.area_min < area < self.area_max:
                line_values = cv2.fitLine(approx, cv.CV_DIST_L2, 0, 0.01, 0.01)
                rect = cv2.boundingRect(approx)
                t = np.sqrt((rect[0]**2 + rect[1]**2) / 2.0)
                lines.append((line_values, t))
                cv2.drawContours(image, contour, -1, (255, 255, 0))

        return lines
    