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
import numpy as np

from CapraVision.server.filters.parameter import  Parameter

class SectionFilter:
    """"""
    
    def __init__(self):
        self.kernel_erode_height = Parameter("Kernel Erode Height", 1, 255, 3)
        self.kernel_erode_width = Parameter("Kernel Erode Width", 1, 255, 3)
        self.kernel_dilate_height = Parameter("Kernel Dilate Height", 1, 255, 5)
        self.kernel_dilate_width = Parameter("Kernel Dilate Width", 1, 255, 5)
        self.sections = Parameter("Sections", 1, 10, 5)
        self.min_area = Parameter("Minimum Area", 1, 65535, 1000)
        self.configure()
        
    def configure(self):
        self.kerode = cv2.getStructuringElement(
                         cv2.MORPH_CROSS, 
                         (int(self.kernel_erode_width.get_current_value()), 
                          int(self.kernel_erode_height.get_current_value())))
        self.kdilate = cv2.getStructuringElement(
                         cv2.MORPH_CROSS, 
                         (int(self.kernel_dilate_width.get_current_value()), 
                          int(self.kernel_dilate_height.get_current_value())))

    def execute(self, image):

        image = cv2.erode(image, self.kerode)

        rows = image.shape[0]
        section_size = rows / int(self.sections.get_current_value())
        for i in xrange(0, int(self.sections.get_current_value())):
            start = (section_size) * i
            end = (section_size) * (i+1)
            if end > rows:
                end = rows
            section = image[start : end]
        
            gray = cv2.split(section)[0]
            contours, _ = cv2.findContours(
                                       gray, 
                                       cv2.RETR_TREE, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
            section = np.zeros(section.shape, np.uint8)
            for contour in contours:
                area = np.abs(cv2.contourArea(contour))
                if area > self.min_area.get_current_value():
                    cv2.drawContours(section, 
                                 [cv2.convexHull(contour)], 
                                 -1, 
                                 (255, 255, 255), 
                                 thickness=-1)        
            image[start: end] = section
        
        
        image = cv2.dilate(image, self.kdilate)
        
        return image
    