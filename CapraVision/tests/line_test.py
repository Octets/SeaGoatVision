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
import math
import numpy as np
import os
import sys

class LineTest:
    
    def __init__(self, image_folder, filterchain):
        self.image_folder = ImageFolder()
        self.image_folder.read_folder(image_folder)
        self.chain = chain.read(filterchain)
        self.precisions = {}
        self.noises = {}
        
    def launch(self):
        for image in self.image_folder:
            file_name = self.image_folder.current_file_name()
            if os.path.exists(file_name + '.map'):
                map = np.fromfile(image + '.map')
                filtered = self.chain.execute(image)
                filtered = self.make_binary_array(filtered)
                precisions[file_name] = self.find_precision(filtered, map)
                noises[file_name] = self.find_noise(filtered, map)
            
    def make_binary_array(self, filtered):
        bin = np.zeros(filtered.shape[0:2], dtype=np.bool)
        bin[filtered > 0] = True
        return bin
    
    def find_precision(self, filtered, map):
        detected = filtered & map
        sum_map = np.sum(map)
        sum_detected = np.sum(detected)
        return (sum_map + sum_detected) / sum_map
    
    def find_noise(self, filtered, map):
        cnt_filtered, _ = cv2.findContours(filtered, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE)
        cnt_map = cv2.findContours(map, 
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
        noise = 0
        for cf in cnt_filtered:
            dist = self.find_dist_between_blob_and_line(cf, cnt_map)
            area = np.abs(cv2.contourArea(cf))
            noise += dist * area
            
        return noise / max_noise(cnt_map, filtered.shape)
    
    def max_noise(self, cnt_map, image_size):
        max_dist = math.sqrt(image_size[0]**2, image_size[1]**2) / 2.0
        max_noise = 0
        for cm in cnt_map:
            area = np.abs(cv2.contourArea(cm))
            max_noise += area * max_dist
        return max_noise
        
    def find_dist_between_blob_and_line(self, blob, cnt_map):
        moment = cv2.moments(cf)
        x = int(moment['m10'] / moment['m00'])
        y = int(moment['m01'] / moment['m00'])
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
        c = len(self.noises)
        s = sum(self.noises.values())
        return s / c
    
    def avg_precision(self):
        c = len(self.precisions)
        s = sum(self.precisions.values())
        return s / c
        