#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
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

import SeaGoatVision.server.filters
from SeaGoatVision.server.filters import utils
from SeaGoatVision.server.filters.dataextract import DataExtract
from SeaGoatVision.commun.param import Param
import ConfigParser
import numpy as np

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def isnumeric(string):
    #TODO in python3, use str.isnumeric()
    try:
        float(string)
        return True
    except ValueError:
        return False

def read(file_name):
    """Open a filtre chain file and load its content in a new filtre chain."""
    filterchain_name = file_name[file_name.rfind("/") + 1:file_name.rfind(".")]
    new_chain = FilterChain(filterchain_name)
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    for section in cfg.sections():
        filtre = SeaGoatVision.server.filters.create_filter(section)
        if not filtre:
            print("Error : The filter %s doesn't exist on filterchain." % (section, filterchain_name))
            continue
        # TODO refaire les parameter seulement
        for member in filtre.__dict__:
            param = getattr(filtre, member)
            if not isinstance(param, Param):
                continue
            try:
                val = cfg.get(section, member)
            except:
                # the file didn't contain the param
                continue
            if val == "True" or val == "False":
                param.set(cfg.getboolean(section, member))
            elif val.isdigit():
                param.set(cfg.getint(section, member))
            elif isnumeric(val):
                f_value = cfg.getfloat(section, member)
                #exception, if the param want int, we will cast it
                if param.get_type() is int:
                    param.set(int(f_value))
                else:
                    param.set(f_value)
            elif val[0] == "(":
                # It's a tuple!
                val = tuple(map(float, val[1:-1].split(',')))
                param.set(val[0], thres_h=val[1])
            else:
                val = '\n'.join([line[1:-1] for line in str.splitlines(val)])
                param.set(val)
        if hasattr(filtre, 'configure'):
            filtre.configure()
        new_chain.add_filter(filtre)
    return new_chain

def write(file_name, chain):
    """Save the content of the filter chain in a file."""
    cfg = ConfigParser.ConfigParser()
    for fname, params in chain.get_params():
        cfg.add_section(fname)
        for param in params:
            value = param.get()
            name = param.get_name()
            if isinstance(value, str):
                value = '\n'.join(['"%s"' % line for line in str.splitlines(value)])
            cfg.set(fname, name, value)
    cfg.write(open(file_name, 'w'))

class FilterChain:
    """ Observable.  Contains the chain of filters to execute on an image.

    The observer must be a method that receive a filter and an image as param.
    The observer method is called after each execution of a filter in the filter chain.
    """
    def __init__(self, filterchain_name):
        self.filters = []
        self.image_observers = {}
        self.filter_output_observers = []
        self.filterchain_name = filterchain_name

    def count(self):
        return len(self.filters)

    def get_name(self):
        return self.filterchain_name

    def get_filter_output_observers(self):
        return self.filter_output_observers

    def get_filter_list(self):
        class Filter: pass
        retValue = []
        for item in self.filters:
            filter = Filter()
            setattr(filter, "name", item.__class__.__name__)
            setattr(filter, "doc", item.__doc__)
            retValue.append(filter)
        return retValue

    def get_params(self, filter=None, filter_name=None):
        if filter_name:
            filter = self.get_filter(name=filter_name)
        if filter:
            return filter.get_params()
        return [(filter.__class__.__name__, filter.get_params()) for filter in self.filters]

    def __getitem__(self, index):
        return self.filters[index]

    def get_filter(self, index=None, name=None):
        if index is not None:
            #TODO not better return self[index] ??
            return self.filters[index]
        elif name is not None:
            lst_filter = [o_filter for o_filter in self.filters if o_filter.__class__.__name__ == name]
            if lst_filter:
                return lst_filter[0]
        return None

    def add_filter(self, filter):
        self.filters.append(filter)

    def remove_filter(self, filter):
        self.filters.remove(filter)

    def reload_filter(self, filtre):
        # example of __module__:
        index = 0
        for item in self.filters:
            if item.__class__.__name__ == filtre:
                # remote observer
                filter_output_obs_copy = self.filter_output_observers[:]
                for output in filter_output_obs_copy:
                    self.remove_filter_output_observer(output)
                # reload the module
                module = my_import(item.__module__)
                reload(module)
                # recreate the instance
                self.filters[index] = getattr(module, item.__class__.__name__)()
                # re-add observer
                for output in filter_output_obs_copy:
                    self.add_filter_output_observer(output)
            index += 1

    def add_image_observer(self, observer, filter_name):
        lstObserver = self.image_observers.get(filter_name, [])
        if lstObserver:
            if observer in lstObserver:
                print("This observer already observer the filter %s" % filter_name)
                return False
            else:
                lstObserver.append(observer)
        else:
            self.image_observers[filter_name] = [observer]
        return True

    def remove_image_observer(self, observer, filter_name):
        lstObserver = self.image_observers.get(filter_name, [])
        if lstObserver:
            if observer in lstObserver:
                lstObserver.remove(observer)
                if not lstObserver:
                    del self.image_observers[filter_name]
                return True

        print("This observer is not in observation list for filter %s" % filter_name)
        return False

    def add_filter_output_observer(self, output):
        self.filter_output_observers.append(output)
        for f in self.filters:
            if isinstance(f, DataExtract):
                f.add_output_observer(output)
        return True

    def remove_filter_output_observer(self, output):
        self.filter_output_observers.remove(output)
        for f in self.filters:
            if isinstance(f, DataExtract):
                f.remove_output_observer(output)
        return True

    def execute(self, image):
        for f in self.filters:
            image = f.execute(image)
            lst_observer = self.image_observers.get(f.__class__.__name__, [])
            for observer in lst_observer:
                # copy the picture because the next filter will modify him
                observer(np.copy(image))
        return image

