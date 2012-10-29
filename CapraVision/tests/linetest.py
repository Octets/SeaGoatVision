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

from CapraVision.sources.implementation.imagefolder import ImageFolder
from CapraVision import chain

import cv2
import cv2.cv as cv
import math
import numpy as np
import os
import sys

class LineTest:
    
    def __init__(self, test_folder, filterchain):
        image_folder = ImageFolder()
        image_folder.return_file_name = True
        image_folder.read_folder(test_folder)
        self.chain = chain.read(filterchain)
        self.testable_images = self.find_testable_images(self.image_folder)
        self.precisions = {}
        self.noises = {}
        
    def find_testable_images(self, image_folder):
        testable_images = {}
        for file_name, image in image_folder:
            if os.path.exists(file_name + '.map'):
                testable_images[file_name] = image
        return testable_images
    
    def launch(self):
        for file_name, image in self.testable_images:
            filtered, map = self.get_test_images(image, file_name)
            self.precisions[file_name] = self.find_precision(filtered, map)
            self.noises[file_name] = self.find_noise(filtered, map)
            
    def get_test_images(self, file_name):
        image = self.testable_images[file_name]
        filtered = self.chain.execute(image)
        filtered = self.make_binary_array(filtered)
        
        map = np.fromfile(file_name + '.map', dtype=np.uint8)
        map = map.reshape(filtered.shape)

        return (filtered, map)
    
    def make_binary_array(self, filtered):
        gray = cv2.cvtColor(filtered, cv.CV_BGR2GRAY)
        bin = np.zeros(gray.shape, dtype=np.uint8)
        bin[gray > 0] = 255
        return bin
    
    def find_precision(self, filtered, map):
        undetected = (filtered & np.invert(map))
        sum_map = np.count_nonzero(map)
        sum_undetected = np.count_nonzero(undetected)
        return (sum_map - sum_undetected) / float(sum_map)
    
    def example_image(self, file_name):
        image = self.testable_images[file_name]
        filtered, map = self.get_test_images(file_name)
        detected = (filtered & map)
        undetected = (filtered & np.invert(map))
        noise = self.remove_line(filtered, map)

        ret_image = np.zeros(image.shape, np.uint8)
        ret_image[:,:,0] = noise
        ret_image[:,:,1] = detected
        ret_image[:,:,2] = undetected
        
        return ret_image
    
    def remove_line(self, filtered, map):
        detected = (filtered & map)
        return (filtered & np.invert(detected))
            
    def find_noise(self, filtered, map):
        filtered = self.remove_line(filtered, map)
        cnt_filtered, _ = cv2.findContours(filtered, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE)
        cnt_map, _ = cv2.findContours(map, 
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
        noise = 0
        for cf in cnt_filtered:
            dist = abs(self.find_dist_between_blob_and_line(cf, cnt_map))
            area = np.abs(cv2.contourArea(cf))
            noise += dist * area
            
        return noise / self.max_noise(cnt_map, filtered.shape)
    
    def max_noise(self, cnt_map, image_size):
        max_dist = math.sqrt(image_size[0]**2 + image_size[1]**2) / 4.0
        max_noise = 0
        for cm in cnt_map:
            area = np.abs(cv2.contourArea(cm)) / 2.0
            max_noise += area * max_dist
        return max_noise
        
    def find_dist_between_blob_and_line(self, cf, cnt_map):
        moment = cv2.moments(cf)
        m00 = moment['m00']
        if m00 <> 0:
            x = int(moment['m10'] / m00)
            y = int(moment['m01'] / m00)
        else:
            x = cf[0][0][0]
            y = cf[0][0][1]
        min_dist = sys.maxint
        for cm in cnt_map:
            dist = cv2.pointPolygonTest(cm, (x, y), True)
            if dist < min_dist:
                min_dist = dist
        return min_dist
    
    def total_images(self):
        count = 0
        for f in self.image_folder.file_names:
            map = f + '.map'
            if os.path.exists(map):
                count += 1
            
        return count
    
    def avg_noise(self):
        c = len(self.noises.values())
        s = sum(self.noises.values())
        return s / c
    
    def avg_precision(self):
        c = len(self.precisions.values())
        s = sum(self.precisions.values())
        return s / c
        