#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
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

import filters
from SeaGoatVision.server.core.filter import Filter
from SeaGoatVision.server.core import utils
from SeaGoatVision.commun.param import Param
from SeaGoatVision.commun.filterchain import *
import ConfigParser
import numpy as np

class FilterChain(object):
    """ Observable.  Contains the chain of filters to execute on an image.

    The observer must be a method that receive a filter and an image as param.
    The observer method is called after each execution of a filter in the filter chain.
    """
    def __init__(self, filterchain_name):
        self.filters = []
        self.image_observers = {}
        self.filter_output_observers = []
        self.filterchain_name = filterchain_name
        self.original_image_observer = []

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
            # TODO not better return self[index] ??
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
                module = utils.module_name(item.__module__)
                reload(module)
                # recreate the instance
                self.filters[index] = getattr(module, item.__class__.__name__)()
                # re-add observer
                for output in filter_output_obs_copy:
                    self.add_filter_output_observer(output)
            index += 1

    def add_image_observer(self, observer, filter_name):
        # Exception for original image
        b_original = False
        if get_filter_original_name() == filter_name:
            b_original = True
            lstObserver = self.original_image_observer
        else:
            lstObserver = self.image_observers.get(filter_name, [])
        if lstObserver:
            if observer in lstObserver:
                print("This observer already observer the filter %s" % filter_name)
                return False
            else:
                lstObserver.append(observer)
        elif not b_original:
            self.image_observers[filter_name] = [observer]
        else:
            lstObserver.append(observer)
        return True

    def remove_image_observer(self, observer, filter_name):
        b_original = False
        if get_filter_original_name() == filter_name:
            b_original = True
            lstObserver = self.original_image_observer
        else:
            lstObserver = self.image_observers.get(filter_name, [])
        if lstObserver:
            if observer in lstObserver:
                lstObserver.remove(observer)
                if not lstObserver and not b_original:
                    del self.image_observers[filter_name]
                return True

        print("This observer is not in observation list for filter %s" % filter_name)
        return False

    def add_filter_output_observer(self, output):
        self.filter_output_observers.append(output)
        for f in self.filters:
            if isinstance(f, Filter):
                f.add_output_observer(output)
        return True

    def remove_filter_output_observer(self, output):
        self.filter_output_observers.remove(output)
        for f in self.filters:
            if isinstance(f, Filter):
                f.remove_output_observer(output)
        return True

    def execute(self, image):
        # TODO Optimize for multiple observer, only one copy
        # first image observator
        if self.original_image_observer:
            for observer in self.original_image_observer:
                observer(np.copy(image))
        for f in self.filters:
            image = f.execute(image)
            lst_observer = self.image_observers.get(f.__class__.__name__, [])
            for observer in lst_observer:
                # copy the picture because the next filter will modify him
                observer(np.copy(image))
        return image
