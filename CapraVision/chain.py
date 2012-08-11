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
Created on 2012-07-26

@author: benoit
'''

import threading, time
import inspect

def open_filter_chain(file_name):
    pass

def save_filter_chain(file_name, chain):
    pass

class ThreadMainLoop(threading.Thread):
    
    def __init__(self, source, filterchain, sleep_time):
        threading.Thread.__init__(self)
        self.source = source
        self.filterchain = filterchain
        self.sleep_time = sleep_time
        self.running = True
        
    def run(self):
        while self.running:
            image = self.source.next_frame()
            self.filterchain.execute(image)
            if self.sleep_time >= 0:
                time.sleep(self.sleep_time)

    def stop(self):
        self.running = False
        
class FilterChain:
    
    def __init__(self):
        self.filters = []
        self.observers = []
        pass
    
    def add_filter(self, filter):
        self.filters.append(filter)
    
    def remove_filter(self, filter):
        self.filters.remove(filter)
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def execute(self, image):
        for f in self.filters:
            if inspect.isfunction(f):
                output = f(image)
            else:
                output = f.execute(image)
            [observer(f, output) for observer in self.observers]
        