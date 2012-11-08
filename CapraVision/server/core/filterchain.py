#! /usr/bin/env python
from CapraVision.server.filters.dataextract import DataExtractor

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

import CapraVision.server.filters

import ConfigParser

def params_list(chain):
    flist = []
    for filtre in chain.filters:
        fname = filtre.__class__.__name__
        params = []
        for name, value in filtre.__dict__.items():
            if name[0] == '_':
                continue
            params.append((name, value))
        flist.append((fname, params))
    return flist

def isnumeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def read(file_name):
    """Open a filtre chain file and load its content in a new filtre chain."""
    new_chain = FilterChain()
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    for section in cfg.sections():
        filtre = CapraVision.server.filters.create_filter(section) 
        for member in filtre.__dict__:
            if member[0] == '_':
                continue
            val = cfg.get(section, member)
            if val == "True" or val == "False":
                filtre.__dict__[member] = cfg.getboolean(section, member)
            elif isnumeric(val):
                filtre.__dict__[member] = cfg.getfloat(section, member)
            else:
                if isinstance(val, str):
                    val = '\n'.join([line[1:-1] for line in str.splitlines(val)])
                filtre.__dict__[member] = val
        if hasattr(filtre, 'configure'):
            filtre.configure()
        new_chain.add_filter(filtre)
    return new_chain

def write(file_name, chain):
    """Save the content of the filter chain in a file."""
    cfg = ConfigParser.ConfigParser()
    for fname, params in params_list(chain):
        cfg.add_section(fname)
        for name, value in params:
            if isinstance(value, str):
                value = '\n'.join(['"%s"' % line for line in str.splitlines(value)])
            cfg.set(fname, name, value)
    cfg.write(open(file_name, 'w'))
    
class FilterChain:
    """ Observable.  Contains the chain of filters to execute on an image.
    
    The observer must be a method that receive a filter and an image as parameter.
    The observer method is called after each execution of a filter in the filter chain.
    """
    def __init__(self):
        self.filters = []
        self.image_observers = [] 
        self.filter_observers = []
    
    def add_filter(self, filtre):
        self.filters.append(filtre)
        self.notify_filter_observers()
        
    def remove_filter(self, filtre):
        self.filters.remove(filtre)
        self.notify_filter_observers()
        
    def move_filter_up(self, filtre):
        i = self.filters.index(filtre)
        if i > 0:
            self.filters[i], self.filters[i-1] = self.filters[i-1], filtre
            self.notify_filter_observers()
        
    def move_filter_down(self, filtre):
        i = self.filters.index(filtre)
        if i < len(self.filters) - 1:
            self.filters[i], self.filters[i+1] = self.filters[i+1], filtre
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
            
    def add_filter_output_observer(self, output):
        for f in self.filters:
            if isinstance(f, DataExtractor):
                f.add_output_observer(output)
            
    def remove_filter_output_observer(self, output):
        for f in self.filters:
            if isinstance(f, DataExtractor):
                f.remove_output_observer(output)
    
    def execute(self, image):
        for f in self.filters:
            image = f.execute(image.copy())
            for observer in self.image_observers:
                observer(f, image)
        return image
