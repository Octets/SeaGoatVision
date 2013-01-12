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
"""Contains helper classes to work with the imageproviders"""

import inspect
import os
import subprocess
import threading

import cv2

import implementation

def close_source(source):
    """Verify if the source has a close() method and call it if so"""
    if hasattr(source, 'close'):
        source.close()

def create_source(source_class):
    """
    Instanciate a source object from the class received in parameter.
    The returned object is thread-safe
    """ 
    return make_source_thread_safe(source_class())

def load_sources():
    """Return a dictionary that contains every Source class from the Sources module"""
    return {name : source_class 
            for name, source_class in vars(implementation).items()
            if inspect.isclass(source_class)}

def find_all_images(folder):
    """Receive a directory as parameter.
        Find all files that are images in all subdirectories.
        Returns a list of those files"""
    images = []
    for root, _, files in os.walk(folder):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext in supported_image_formats():
                images.append(os.path.join(root,filename))
    list.sort(images)
    return images

def create_image_as_png(file_name):
    """Receive a filename name as parameter.
        The filename is loaded and saved as a png.
        The old filename is not modified."""
    if os.path.splitext(file_name)[1] == '.png':
        return
    img = cv2.imread(file_name)
    new_file_name, _ = os.path.splitext(file_name)
    cv2.imwrite(new_file_name + '.png', img)
    
def make_source_thread_safe(source):
    return ThreadSafeSourceWrapper(source)
        
def supported_image_formats():
    """Standard image formats supported by OpenCV"""
    
    return (
            '.bmp', 
            '.jpeg', 
            '.jpg', 
            '.png', 
            '.pbm', 
            '.pgm', 
            '.ppm', 
            '.tiff', 
            '.tif'
            )

def supported_video_formats():
    return ffmpeg_video_formats()

def ffmpeg_video_formats():
    """Finds all supported video formats of ffmpeg"""
    
    p = subprocess.Popen(('avconv', '-formats'), stdout=subprocess.PIPE)
    lines = p.stdout.readlines()

    supported = []
    formats = False
    for line in lines:
        if formats:
            exts = line[4:].split(' ')[0].split(',')
            for ext in exts:
                if ext == 'mkvtimestamp_v2':
                    supported.append('.mkv')
                else:
                    supported.append('.' + ext)
        if line == ' --\n':
            formats = True
    return supported

class ThreadSafeSourceWrapper:
    """This is a wrapper around the sources to make it thread-safe.
    The goal of this class is to remove boiler plate code from the sources.
    Each methods from the base source must be defined.
    """
    
    def __init__(self, source):
        self.source = source
        self.lock = threading.Lock()
        self.__class__.__name__ = source.__class__.__name__
        
    def __getattr__(self, name):
        return getattr(self.source, name)
                
    def __iter__(self):
        return self
    
    def next(self):
        return self.thread_safe_call(self.source.next)
    
    def close(self):
        if hasattr(self.source, 'close'):
            return self.thread_safe_call(self.source.close)
    
    def thread_safe_call(self, method):
        """
        Receive a method in parameter.
        The method is called after acquiring a lock
        """
        self.lock.acquire()
        try:
            return method()
        finally:
            self.lock.release()
