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

from SeaGoatVision.server.core.filter import Filter
from SeaGoatVision.server.core import utils
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons.keys import *
import cv2
import cv2.cv as cv
import ConfigParser
import numpy as np
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class FilterChain(object):
    """ Observable.  Contains the chain of filters to execute on an image.

    The observer must be a method that receive a filter and an image as param.
    The observer method is called after each execution of a filter in the filter chain.
    """
    def __init__(self, filterchain_name, serialize=None, default_media_name=None):
        # to limit the infini import, we import in the init
        from resource import Resource
        self.resource = Resource()

        self.filters = []
        # {"filter_name":[observator,]}
        self.image_observers = {}
        self.filter_output_observers = []
        self.filterchain_name = filterchain_name
        self.original_image_observer = []
        self.dct_global_param = {}
        # If starting filterchain with empty media_name, we take the default media
        self.default_media_name = default_media_name

        if serialize:
            self.deserialize(filterchain_name, serialize)
        else:
            # add default filter
            self.add_filter(Filter(get_empty_filter_name()))

    def destroy(self):
        # clean everything!
        for obs in self.filter_output_observers:
            self.remove_filter_output_observer(obs)

        for obs in self.original_image_observer:
            self.remove_image_observer(obs, get_filter_original_name())

        for filter_name, lst_obs in self.image_observers.items():
            for obs in lst_obs:
                self.remove_image_observer(obs, filter_name)

        for filter in self.filters:
            filter.destroy()

    def serialize(self):
        # Keep list of filter with param
        dct = {"lst_filter":[filter.serialize() for filter in self.filters if filter.name != get_empty_filter_name()]}
        if self.default_media_name:
            dct["default_media_name"] = self.default_media_name
        return dct

    def deserialize(self, name, value):
        status = True
        self.filterchain_name = name
        lst_filter = value.get("lst_filter", [])
        self.default_media_name = value.get("default_media_name", None)
        self.filters = []
        index = 0
        # add default filter
        self.add_filter(Filter(get_empty_filter_name()))
        for filter_to_ser in lst_filter:
            filter_name = filter_to_ser.get("filter_name", None)
            o_filter = self.resource.create_filter(filter_name, index)
            index += 1
            if not o_filter:
                log.print_function(logger.warning, "Cannot create filter %s, maybe it not exists." % filter_name)
                continue
            status &= o_filter.deserialize(filter_to_ser)
            self.add_filter(o_filter)
        if status:
            log.print_function(logger.info, "Deserialize filterchain %s success." % name)
        else:
            log.print_function(logger.warning, "Deserialize filterchain %s failed." % name)
        return status

    def count(self):
        return len(self.filters)

    def get_name(self):
        return self.filterchain_name

    def get_default_media_name(self):
        return self.default_media_name

    def set_default_media_name(self, name):
        self.default_media_name = name

    def get_filter_output_observers(self):
        return self.filter_output_observers

    def get_filter_list(self):
        class Filter: pass
        retValue = []
        for item in self.filters:
            filter = Filter()
            setattr(filter, "name", item.get_name())
            setattr(filter, "doc", item.__doc__)
            retValue.append(filter)
        return retValue

    def get_params(self, filter=None, filter_name=None):
        if filter_name:
            filter = self.get_filter(name=filter_name)
            if not filter:
                return None
        if filter:
            return filter.get_params()
        return [(filter.get_name(), filter.get_params()) for filter in self.filters]

    def __getitem__(self, index):
        return self.filters[index]

    def get_filter(self, index=None, name=None):
        if index is not None:
            # TODO not better return self[index] ??
            return self.filters[index]
        elif name is not None:
            lst_filter = [o_filter for o_filter in self.filters if o_filter.get_name() == name]
            if lst_filter:
                return lst_filter[0]
        return None

    def add_filter(self, filter):
        self.filters.append(filter)
        filter.set_global_params(self.dct_global_param)

    def remove_filter(self, filter):
        self.filters.remove(filter)

    def reload_filter(self, filtre):
        # TODO: not working because module name change
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
                log.print_function(logger.warning, "This observer already observer the filter %s" % filter_name)
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

        log.print_function(logger.warning, "This observer is not in observation list for filter %s" % filter_name)
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
        original_image = np.copy(image);
        # first image observator
        if self.original_image_observer:
            self.send_image(original_image, self.original_image_observer)

        for f in self.filters:
            f.set_original_image(original_image)
            try:
                image = f.execute(image)
            except Exception as e:
                msg = "(Exec exception Filter %s) %s" % (f.get_name(), e)
                log.printerror_stacktrace(logger, msg, check_duplicate=True)
                break

            lst_observer = self.image_observers.get(f.get_name(), [])
            self.send_image(image, lst_observer)
        return image

    def send_image(self, image, lst_observer):
        if type(image) is not np.ndarray or not image.size:
            return
        # copy the picture because the next filter will modify him
        # transform it in rgb
        image2 = np.copy(image)
        cv2.cvtColor(np.copy(image), cv.CV_BGR2RGB, image2)
        for observer in lst_observer:
            observer(image2)
