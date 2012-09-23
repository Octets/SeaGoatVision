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
"""Contains helper classes to work with the sources"""

import inspect, threading, sys
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

def make_source_thread_safe(source):
    return ThreadSafeSourceWrapper(source)
        
def supported_image_formats():
    return ['bmp', 'jpeg', 'jpg', 'png', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']

class ThreadSafeSourceWrapper:
    """This is a wrapper around the sources to make it thread-safe.
    The goal of this class is to remove boiler plate code from the sources.
    Each methods from the base source must be defined.
    """
    
    def __init__(self, source):
        self.source = source
        self.lock = threading.Lock()
        
    def __getattr__(self, name):
        return getattr(self.source, name)
    
    def __iter__(self):
        return self
    
    def next(self):
        return self.thread_safe_call(self.source.next)
    
    def close(self):
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
