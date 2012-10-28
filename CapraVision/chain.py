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

"""Contains the FilterChain class and helper functions to work with the filter chain."""

import ConfigParser
import inspect
import threading
import time

import filters

def isnumeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def read(file_name):
    """Open a filter chain file and load its content in a new filter chain."""
    new_chain = FilterChain()
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    for section in cfg.sections():
        filter = filters.create_filter(section) 
        for member in filter.__dict__:
            if member[0] == '_':
                continue
            val = cfg.get(section, member)
            if val == "True" or val == "False":
                filter.__dict__[member] = cfg.getboolean(section, member)
            elif isnumeric(val):
                filter.__dict__[member] = cfg.getfloat(section, member)
            else:
                filter.__dict__[member] = val
        if hasattr(filter, 'configure'):
            filter.configure()
        new_chain.add_filter(filter)
    return new_chain

def write(file_name, chain):
    """Save the content of the filter chain in a file."""
    cfg = ConfigParser.ConfigParser()
    for filter in chain.filters:
        fname = filter.__class__.__name__
        cfg.add_section(fname)
        for name, value in filter.__dict__.items():
            if name[0] == '_':
                continue
            cfg.set(fname, name, value)
    cfg.write(open(file_name, 'w'))
    
class ThreadMainLoop(threading.Thread):
    """Main thread to process the images.
    
    Args:
        source: the source to receive images from.
        filterchain: the configured filterchain
        sleep_time: time to wait in seconds before getting the next image
    """
    def __init__(self, source, sleep_time):
        threading.Thread.__init__(self)
        self.daemon = True
        self.source = source
        self.sleep_time = sleep_time
        self.running = False
        self.observers = []
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def run(self):
        self.running = True
        for image in self.source:
            if image is None:
                time.sleep(self.sleep_time)
                continue
            self.notify_observers(image)
            if not self.running:
                break
            if self.sleep_time >= 0:
                time.sleep(self.sleep_time)
        self.running = False
        
    def notify_observers(self, image):
        for observer in self.observers:
            observer(image)
            
    def stop(self):
        self.running = False
        
class FilterChain:
    """ Observable.  Contains the chain of filters to execute on an image.
    
    The observer must be a method that receive a filter and an image as parameter.
    The observer method is called after each execution of a filter in the filter chain.
    """
    def __init__(self):
        self.filters = []
        self.image_observers = [] 
        self.filter_observers = []
    
    def add_filter(self, filter):
        self.filters.append(filter)
        self.notify_filter_observers()
        
    def remove_filter(self, filter):
        self.filters.remove(filter)
        self.notify_filter_observers()
        
    def move_filter_up(self, filter):
        i = self.filters.index(filter)
        if i > 0:
            self.filters[i], self.filters[i-1] = self.filters[i-1], filter
            self.notify_filter_observers()
        
    def move_filter_down(self, filter):
        i = self.filters.index(filter)
        if i < len(self.filters) - 1:
            self.filters[i], self.filters[i+1] = self.filters[i+1], filter
            self.notify_filter_observers()
    
    def add_image_observer(self, observer):
        self.image_observers.append(observer)
        
    def remove_image_observer(self, observer):
        self.image_observers.remove(observer)
        
    def add_filter_observer(self, observer):
        self.filter_observers.append(observer)
        
    def remove_filter_observer(self, observer):
        self.filter_observers.remove(observer)
        
    def notify_filter_observers(self):
        for observer in self.filter_observers:
            observer()
    
    def execute(self, image):
        for f in self.filters:
            image = f.execute(image.copy())
            for observer in self.image_observers:
                observer(f, image)
        return image
    