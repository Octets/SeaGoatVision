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

import os
from time import gmtime, strftime

import cv
import cv2

class Recorder:
    
    def __init__(self):
        self.savepath = ''
        self.saver_class = None
        self.savers = {}
        self.running = False
    
    def set_saver_class(self, saver):
        self.saver_class = saver
        
    def set_save_path(self, savepath):
        self.savepath = savepath
        
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False
    
    def add_filter(self, filtre):
        self.savers[filtre] = self.saver_class(self.savepath, filtre)
    
    def remove_filter(self, filtre):
        del self.savers[filtre]
    
    def filter_observer(self, filtre, image):
        if not self.running:
            return
        
        if self.saver is not None and filtre in self.filters.keys:
            self.saver.save(filtre, image)
    
class SimpleRecorder:
    
    def __init__(self, fps, size, thread):
        self.thread = None
        if os.path.exists(self.get_record_path()):
            self.video = cv2.VideoWriter(self.get_record_path() + "/" + self.get_file_name(), 
                        cv.CV_FOURCC('D','I','B',' '), fps, size, True)
            self.thread = thread
            thread.add_observer(self.thread_observer)
        else:
            print "Error: record path not available"
        
    def thread_observer(self, image):
        self.video.write(image)
    
    def stop(self):
        self.thread.remove_observer(self.thread_observer)
    
    def get_record_path(self):
        path = os.path.join('..', 'videos')
        return path
    
    def get_file_name(self):
        name = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        return name + '.avi'

class PNGRecorder:
    
    def __init__(self, fps, size, thread):
        self.time = gmtime()
        self.thread = thread
        os.makedirs(self.get_record_path())
            
        self.number = 0
        thread.add_observer(self.thread_observer)
        
    def thread_observer(self, image):
        cv2.imwrite(os.path.join(self.get_record_path(), 
                                 self.get_file_name()), image)
    
    def stop(self):
        self.thread.remove_observer(self.thread_observer)
    
    def get_record_path(self):
        path = os.path.join('..', 'videos', self.get_dir_name())
        return path
    
    def get_dir_name(self):
        name = strftime("%Y_%m_%d_%H_%M_%S", self.time)
        return name

    def get_file_name(self):
        self.number += 1
        return str.rjust(str(self.number), 10, '0') + '.png'
                