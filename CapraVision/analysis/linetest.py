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

from CapraVision.imageproviders.implementation.imagefolder import ImageFolder
from CapraVision.core import filterchain

import cv2
import cv2.cv as cv
import math
import numpy as np
import os
import sys

class LineTest:
    """This class test the precision of the detection of lines of a filterchain.
        It uses a folder that contains image files and mappings files.  The
        mapping files contains the information about 
        the lines inside the images
    
    After creation, the launch() method should be called to execute the test.    
    """
        
    def __init__(self, test_folder, fchain):
        """Creates the object.
        Args:
            test_folder: Complete path to the folder that contains the 
            test images and its mapping.
            filterchain: Complete path to the filterchain file."""
            
        image_folder = self.create_image_folder_source(test_folder)
        self.fchain = filterchain.read(fchain)
        self.testable_images = self.find_testable_images(image_folder)
        
        # These dictionaries contains the values calculated by the test.
        # Keys: image file name.
        # Values: float representing the percentage. 
        self.precisions = {}
        self.noises = {}

    def avg_noise(self):
        """Returns the calculated average noise"""
        c = len(self.noises.values())
        s = sum(self.noises.values())
        return s / c
    
    def avg_precision(self):
        """Returns the calculated averaged precision"""
        c = len(self.precisions.values())
        s = sum(self.precisions.values())
        return s / c
    
    def create_image_folder_source(self, test_folder):
        image_folder = ImageFolder()
        image_folder.return_file_name = True
        image_folder.read_folder(test_folder)
        return image_folder
    
    def example_image(self, file_name):
        """Returns an example of what is correctly detected,
            noise and what is not detected.  The size of the image is 320x240.
        Args:
            file_name: the complete path to the image in the test folder."""
        image = self.testable_images[file_name]
        filtered, map = self.get_test_images(file_name)
        detected = (filtered & map)
        undetected = (filtered & np.invert(map))
        noise = self.remove_line(filtered, map)

        ret_image = np.zeros(image.shape, np.uint8)
        ret_image[:,:,0] = noise 
        #ret_image[:,:,1] = detected 
        #ret_image[:,:,2] = undetected 
        
        return cv2.resize(ret_image, (320, 240))
    
    def find_dist_between_blob_and_line(self, cf, cnt_map):
        """Returns the minimum distance between a blob and a line.
        Args:
            cf: the contour of the blob
            cnt_map: the contour of the line
        """
        
        # Find the center of the blob
        moment = cv2.moments(cf)
        m00 = moment['m00']
        if m00 <> 0:
            x = int(moment['m10'] / m00)
            y = int(moment['m01'] / m00)
        else:
            x = cf[0][0][0]
            y = cf[0][0][1]
        min_dist = sys.maxint
        
        # If there are many lines, we find the closest one
        for cm in cnt_map:
            dist = cv2.pointPolygonTest(cm, (x, y), True)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def find_noise(self, filtered, map):
        """Returns the percentage of noise in the image
        Args:
            filtered: the filtered image from the filterchain
            map: the array containing the line information"""
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
    
    def find_precision(self, filtered, map):
        """Returns the precision of the line detection
        Args:
            filtered: the filtered image from the filterchain
            map: the array containing the line information"""
        undetected = (filtered & np.invert(map))
        sum_map = np.count_nonzero(map)
        sum_undetected = np.count_nonzero(undetected)
        return (sum_map - sum_undetected) / float(sum_map)
    
    def find_testable_images(self, image_folder):
        """Find all the images that have a mapping file associated with them
        Args:
            image_folder: an ImageFolder source object"""
        testable_images = {}
        for file_name, image in image_folder:
            if os.path.exists(file_name + '.map'):
                testable_images[file_name] = image
        return testable_images
    
    def get_test_images(self, file_name):
        """Create the image and its map from the file name.
        Args:
            file_name: complete path to an image in the test folder
        Returns:
            A tuple containing the filtered image from the filterchain and 
            the mapping of the lines in the image
        """
        image = self.testable_images[file_name]
        filtered = self.fchain.execute(image)
        filtered = self.make_binary_array(filtered)
        
        map = np.fromfile(file_name + '.map', dtype=np.uint8)
        map = map.reshape(filtered.shape)

        return (filtered, map)

    def launch(self):
        """Execute the test"""
        for file_name, image in self.testable_images.items():
            filtered, map = self.get_test_images(file_name)
            self.precisions[file_name] = self.find_precision(filtered, map)
            self.noises[file_name] = self.find_noise(filtered, map)
                
    def make_binary_array(self, filtered):
        """Convert a filtered image to binary
        pixel = 0 -> 0
        pixel > 0 -> 255"""
        gray = cv2.cvtColor(filtered, cv.CV_BGR2GRAY)
        bin = np.zeros(gray.shape, dtype=np.uint8)
        bin[gray > 0] = 255
        return bin
                        
    def max_noise(self, cnt_map, image_size):
        """Returns the max noise value for the image.
        Args:
            cnt_map: the contour of the lines
            image_size: the size of the image eg (640, 480)"""
        max_dist = math.sqrt(image_size[0]**2 + image_size[1]**2) / 4.0
        max_noise = 0
        for cm in cnt_map:
            area = np.abs(cv2.contourArea(cm)) / 2.0
            max_noise += area * max_dist
        return max_noise

    def original_image(self, file_name):
        """Returns the original image scaled to 320x240"""
        return cv2.resize(self.testable_images[file_name], (320, 240))

    def remove_line(self, filtered, map):
        """Remove the line from a filtered image using the map"""
        detected = (filtered & map)
        return (filtered & np.invert(detected))
    
    def total_images(self):
        """Returns the amount of testable images in the test folder"""
        return len(self.testable_images)
            