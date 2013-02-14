#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of CapraVision.
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
import os

class VideoRecorder():
    
    def __init__(self, savepath, filtre, fps=30):
        self.videowriter = None
        self.savepath = savepath
        self.filtre = filtre
        self.fps = fps
        
    def file_name(self):
        return os.path.join(
            self.savepath, 
            self.filtre.__class__.__name__ + '.avi')
        
    def init_writer(self, image):
        return cv2.VideoWriter(
            self.file_name(),
            cv2.cv.CV_FOURCC('F', 'L', 'V', '1'), 
            self.fps, 
            (image.shape[1], image.shape[0])
        )
        
    def save(self, image):
        if self.videowriter is None:
            self.videowriter = self.init_writer(image)
        self.videowriter.write(image)
        
    