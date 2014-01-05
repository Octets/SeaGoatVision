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
from SeaGoatVision.commons import keys
import cv2
from cv2 import cv
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
        self.dct_media_param = {}
        # If starting filterchain with empty media_name, we take the default
        # media
        self.default_media_name = default_media_name

        if serialize:
            self.deserialize(filterchain_name, serialize)
        else:
            # add default filter
            self.add_filter(Filter(keys.get_empty_filter_name()))

    def destroy(self):
        # clean everything!
        for obs in self.filter_output_observers:
            self.remove_filter_output_observer(obs)

        for obs in self.original_image_observer:
            self.remove_image_observer(obs, keys.get_filter_original_name())

        for filter_name, lst_obs in self.image_observers.items():
            for obs in lst_obs:
                self.remove_image_observer(obs, filter_name)

        for o_filter in self.filters:
            o_filter.destroy()

    def serialize(self):
        # Keep list of filter with param
        dct = {"lst_filter": [o_filter.serialize()
                              for o_filter in self.filters if o_filter.name != keys.get_empty_filter_name()]}
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
        self.add_filter(Filter(keys.get_empty_filter_name()))
        for filter_to_ser in lst_filter:
            filter_name = filter_to_ser.get("filter_name", None)
            o_filter = self.resource.create_filter(filter_name, index)
            index += 1
            if not o_filter:
                log.print_function(
                    logger.warning,
                    "Cannot create filter %s, maybe it not exists." %
                    filter_name)
                continue
            status &= o_filter.deserialize(filter_to_ser)
            self.add_filter(o_filter)
        if status:
            log.print_function(
                logger.info,
                "Deserialize filterchain %s success." %
                name)
        else:
            log.print_function(
                logger.warning,
                "Deserialize filterchain %s failed." %
                name)
        return status

    def deserialize_update(self, name, value):
        status = True
        self.filterchain_name = name
        lst_filter = value.get("lst_filter", [])
        if self.default_media_name is None:
            self.default_media_name = value.get("default_media_name", None)

        for o_filter in self.filters:
            # find is appropriate filter if exist
            for filter_ser in lst_filter:
                if filter_ser.get("filter_name", None) == o_filter.get_code_name():
                    status &= o_filter.deserialize(filter_ser)
        return status

    def count(self):
        return len(self.filters)

    def set_media_param(self, dct_media_param):
        self.dct_media_param = dct_media_param
        for item in self.filters:
            item.set_media_param(dct_media_param)

    def get_name(self):
        return self.filterchain_name

    def get_default_media_name(self):
        return self.default_media_name

    def set_default_media_name(self, name):
        self.default_media_name = name

    def get_filter_output_observers(self):
        return self.filter_output_observers

    def get_filter_list(self):
        class Filter:
            def __init__(self):
                pass

        ret_value = []
        for item in self.filters:
            ret_value.append(item.serialize_info())
        return ret_value

    def get_params(self, o_filter=None, filter_name=None, param_name=None):
        if filter_name:
            o_filter = self.get_filter(name=filter_name)
            if not o_filter:
                return None
        if o_filter:
            if param_name:
                return o_filter.get_params(param_name=param_name)
            return o_filter.get_params()
        return [(o_filter.get_name(), o_filter.get_params()) for o_filter in self.filters]

    def __getitem__(self, index):
        return self.filters[index]

    def get_filter(self, index=None, name=None):
        return_data = None
        if index is not None:
            # TODO not better return self[index] ??
            return_data = self.filters[index]
        elif name is not None:
            lst_filter = [
                o_filter for o_filter in self.filters if o_filter.get_name() == name]
            if lst_filter:
                return_data = lst_filter[0]
        else:
            return_data = self.filters
        return return_data

    def get_filter_name(self):
        return [o_filter.get_name() for o_filter in self.filters]

    def add_filter(self, o_filter):
        self.filters.append(o_filter)
        o_filter.set_global_params(self.dct_global_param)

    def remove_filter(self, o_filter):
        self.filters.remove(o_filter)

    def reload_filter(self, o_filter):
        # TODO: not working because module name change
        # example of __module__:
        index = 0
        for item in self.filters:
            if item.__class__.__name__ == o_filter.__class__.__name__:
                # remote observer
                filter_output_obs_copy = self.filter_output_observers[:]
                for output in filter_output_obs_copy:
                    self.remove_filter_output_observer(output)
                    # recreate the instance
                # index -1 to ignore the default filter
                o_filter.set_name("%s-%d" % (o_filter.get_name(), index - 1))
                obj = self.filters[index]
                self.filters[index] = o_filter
                del obj
                # re-add observer
                for output in filter_output_obs_copy:
                    self.add_filter_output_observer(output)
            index += 1

    def add_image_observer(self, observer, filter_name):
        # Exception for original image
        b_original = False
        if keys.get_filter_original_name() == filter_name:
            b_original = True
            lst_observer = self.original_image_observer
        else:
            lst_observer = self.image_observers.get(filter_name, [])
        if lst_observer:
            if observer in lst_observer:
                log.print_function(
                    logger.warning,
                    "This observer already observer the filter %s" %
                    filter_name)
                return False
            else:
                lst_observer.append(observer)
        elif not b_original:
            self.image_observers[filter_name] = [observer]
        else:
            lst_observer.append(observer)
        return True

    def remove_image_observer(self, observer, filter_name):
        b_original = False
        if keys.get_filter_original_name() == filter_name:
            b_original = True
            lst_observer = self.original_image_observer
        else:
            lst_observer = self.image_observers.get(filter_name, [])
        if lst_observer:
            if observer in lst_observer:
                lst_observer.remove(observer)
                if not lst_observer and not b_original:
                    del self.image_observers[filter_name]
                return True

        log.print_function(
            logger.warning,
            "This observer is not in observation list for filter %s" %
            filter_name)
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
        original_image = np.copy(image)
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
            if lst_observer:
                self.send_image(image, lst_observer)
        return image

    def send_image(self, image, lst_observer):
        if not isinstance(image, np.ndarray) or not image.size or image.ndim != 3:
            return
            # copy the picture because the next filter will modify him
        # transform it in rgb
        image2 = np.copy(image)
        cv2.cvtColor(np.copy(image), cv.CV_BGR2RGB, image2)
        for observer in lst_observer:
            observer(image2)
