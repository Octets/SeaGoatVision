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

import inspect
import types
import CapraVision.server.filters.implementation

def add_getters_setters(filtre):
    def create_getter(param):
        def getter(self):
            return self.__dict__[param]
        return getter
    
    def create_setter(param):
        def setter(self, value):
            self.__dict__[param] = value
        return setter
    
    params = list_params_from_filter(filtre)
    for param, _ in params:
        if not hasattr(filtre, 'get_' + param):
            filtre.__dict__['get_' + param] = types.MethodType(create_getter(param), filtre)
        if not hasattr(filtre, 'set_' + param):
            filtre.__dict__['set_' + param] = types.MethodType(create_setter(param), filtre)
    return filtre

def load_filters():
    return {name: filtre 
        for name, filtre in vars(CapraVision.server.filters.implementation).items()
            if inspect.isclass(filtre)}

def create_filter(filter_name):
    for name, filtre in load_filters().items():
        if name == filter_name:
            f = filtre()
            return add_getters_setters(f)
    return None
        
def list_params_from_filter(filtre):
    return [(name, value) for name, value in filtre.__dict__.items() if name[0] != '_']

def get_filter_from_filterName(filter_name):
    return load_filters().get(filter_name, None)
    
    
    
