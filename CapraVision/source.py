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
Created on 2012-08-01

@author: benoit
'''

import cv2
import os

class ImageFolder:
    
    def __init__(self, folder_name):
        self.folder_name = folder_name
        
    def next_frame(self):
        for f in os.listdir(self.folder_name):
            image = cv2.imread(f)
            if image <> None:
                yield image

class Webcam:
            
    def __init__(self, camera_number):
        self.run = True
        self.video = cv2.VideoCapture(camera_number)
        #self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        #self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    def __del__(self):
        self.close()
        
    def next_frame(self):
        run, image = self.video.read()
        return image
    
    def close(self):
        self.video.release()
        