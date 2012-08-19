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

"""
This module contains the code for the sources.
Sources are objects that returns images.  
It can be a a webcam, list of files from the hard drive or anything else.
"""

import cv2
import os

class ImageFolder:
    
    def __init__(self):
        self.folder_name = '.'
        
    def next_frame(self):
        for f in os.listdir(self.folder_name):
            image = cv2.imread(f)
            if image <> None:
                yield image
        
class Webcam:
    """Return images from the webcam.""" 
    def __init__(self):
        self.run = True
        self.camera_number = 0
        self.video = cv2.VideoCapture(self.camera_number)
        #self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        #self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        
    def next_frame(self):
        run, image = self.video.read()
        return image
        
    def close(self):
        self.video.release()
        