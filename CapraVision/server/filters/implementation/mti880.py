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
import cv2.cv as cv

import numpy as np

from CapraVision.server.filters.parameter import  Parameter
from CapraVision.server.filters.dataextract import  DataExtractor

class MTI880(DataExtractor):
    
    def __init__(self):
        DataExtractor.__init__(self)
        self.hue_min = 113
        self.hue_max = 255
        self.area_min = 600
        
        self.normal_hand = 0
        self.extended_hand = 0
        self.closed_hand = 0
        
        self._capture_normal_hand = False
        self._capture_extended_hand = False
        self._capture_closed_hand = False
        
        self._calibrate_hue = False
        self.accumulate = []
        
    def execute(self, image):
        image = cv2.cvtColor(image, cv2.cv.CV_BGR2HSV)
        h, _, _ = cv2.split(image)
        image[h < self.hue_min] *= 0
        image[h > self.hue_max] *= 0
        
        #image[image > 0] = 255
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cnt, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image *= 0
        area, c = self.detect_biggest_area(gray)
        
        if self._calibrate_hue and c is not None:
            self.hue_min += 1
        elif self._calibrate_hue:
            self._calibrate_hue = False
        
        self.calibrate_closed_hand(area)
        self.calibrate_extended_hand(area)
        self.calibrate_normal_hand(area)
        
        if c is not None:
            hull = cv2.convexHull(c)
            cv2.drawContours(image, [hull],-1, (255,255,255), -1)
            self.notify_output_observers(str(area) + "\n")
                
        return image
         
    def detect_biggest_area(self, gray):
        cnt, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        maxarea = 0
        maxcnt = None
        for c in cnt:
            approx = cv2.approxPolyDP(c, 0, False)
            area = np.abs(cv2.contourArea(c))
            if area > maxarea:
                maxarea = area
                maxcnt = c
        return (maxarea, maxcnt)
    
    def calibrate_normal_hand(self, area):
        if self._capture_normal_hand:
            self.accumulate.append(area)
        if len(self.accumulate) == 10:
            total = 0
            for val in self.accumulate:
                total += val
            self._capture_normal_hand = False
            self.normal_hand = total / 10
            
    def calibrate_extended_hand(self):
        if self._capture_extended_hand:
            self.accumulate.append(area)
        if len(self.accumulate) == 10:
            total = 0
            for val in self.accumulate:
                total += val
            self._capture_extended_hand = False
            self.extended_hand = total / 10
            
    def calibrate_closed_hand(self):
        if self._capture_closed_hand:
            self.accumulate.append(area)
        if len(self.accumulate) == 10:
            total = 0
            for val in self.accumulate:
                total += val
            self._capture_closed_hand = False
            self.closed_hand = total / 10
            
    