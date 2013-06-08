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
import math
import numpy as np

from CapraVision.server.filters import dataextract
from CapraVision.server.filters.parameter import  Parameter

class LineOrientation(dataextract.DataExtractor):
    """Port of the old line detection code"""
    
    filter_name = "LineOrientation:"
    
    def __init__(self):
        dataextract.DataExtractor.__init__(self)
        self.area_min = Parameter("Area Min",1,100000,300)
        self.area_max = Parameter("Area Max",1,100000,35000)
    
        self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3), (0,0))
                
    def execute(self, image):
        image_threshold = cv2.split(image)[0]
        image_morphology = cv2.morphologyEx(
                    image_threshold, cv2.MORPH_CLOSE, self._kernel, iterations=1)
                
        contours, _ = cv2.findContours(
                                            image_morphology, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE)
        lines = self.find_lines(contours, image)
        self.draw_lines(lines, image)
        self.send_lines(lines)
        
        return image
    
    def draw_lines(self, lines, image):
        for l in lines:
            x1, y1, x2, y2 = l
            point1 = (x1,y1)
            point2 = (x2,y2)
            cv2.line(image, point1, point2, (0, 0, 255), 3, -1)
            #cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            
    def send_lines(self, lines):
        toSend = ""
        for l in lines:
            x1, y1, x2, y2 = l
            toSend += self.filter_name + " x1=" + str(int(x1)) + " y1=" + str(int(y1)) + " x2=" + str(int(x2)) + " y2=" + str(int(y2)) + " \n"
            
        toSend += "=\n"
        self.notify_output_observers(toSend)
    
    def is_point_intersecting (self, point, image):
        x,y = point
        if x >= 0 and y >= 0 and x < image.shape[1] and y < image.shape[0]:
            if not image[y][x][0] == 0:
                return True
        return False
                       
    def find_lines(self, contours, image):
        lines = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0, False)
            area = np.abs(cv2.contourArea(contour))
            
            if self.area_min.get_current_value() < area < self.area_max.get_current_value():
                line_values = cv2.fitLine(approx, cv.CV_DIST_L2, 0, 0.01, 0.01)
                rect = cv2.boundingRect(approx)
                t0 = t1 = math.sqrt((rect[2]**2 + rect[3]**2) / 2.0)
                
                vx,vy,x,y = line_values

                # CHEAP FIX
                limit1Found = limit2Found = False

                while not (limit1Found and limit2Found) and t0 > 0 and t1 > 0:
                    if not limit1Found:
                        if not self.is_point_intersecting((int(x - t0 * vx),int( y - t0 * vy)), image):
                            t0 = t0 - 20
                        else:
                            limit1Found = True
                            
                    if not limit2Found:
                        if not self.is_point_intersecting((int(x + t1 * vx),int( y + t1 * vy)), image):
                            t1 = t1 - 20 
                        else:
                            limit2Found = True     
                
                line = (x - t0 * vx, y - t0 * vy, x + t1 * vx, y + t1 * vy )
                
                lines.append(line)
                cv2.drawContours(image, contour, -1, (255, 255, 0))

        return lines
    