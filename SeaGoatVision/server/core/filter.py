#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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

from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class Filter(object):
    def __init__(self, name=None):
        self._output_observers = list()
        self.original_image = None
        self.name = name
        self.dct_global_param = {}
        self.dct_media_param = {}

    def serialize(self, is_config=False, is_info=False):
        if is_info:
            return {"name": self.name, "doc": self.__doc__}
        else:
            return {"filter_name": self.__class__.__name__,
                    "lst_param": [param.serialize(is_config=is_config) for param in
                                  self.get_params()]}

    def deserialize(self, value):
        status = True
        for param_ser in value.get("lst_param"):
            param_name = param_ser.get("name", None)
            if not param_name:
                continue
            param = self.get_params(param_name=param_name)
            if param:
                status &= param.deserialize(param_ser)
        return status

    def get_name(self):
        return self.name

    def get_code_name(self):
        key = "-"
        if key in self.name:
            return self.name[:self.name.rfind("-")]
        return self.name

    def set_name(self, name):
        self.name = name

    def destroy(self):
        # edit me
        # It's called just before to be destroyed
        pass

    def configure(self):
        # edit me
        pass

    def execute(self, image):
        # edit me
        return image

    def set_global_params(self, dct_global_param):
        # complete the list and point on it
        for key, param in self.dct_global_param.items():
            if key in dct_global_param:
                log.print_function(logger.error, "Duplicate key on dct_global_param : %s", key)
                continue
            dct_global_param[key] = param
        self.dct_global_param = dct_global_param
        self.set_global_params_cpp(self.dct_global_param)

    def set_global_params_cpp(self, dct_global_param):
        pass

    def add_global_params(self, param):
        name = param.get_name()
        if name in self.dct_global_param:
            log.print_function(logger.error, "This param is already in the list : %s", name)
            return
        self.dct_global_param[name] = param

    def get_global_params(self, param_name):
        return self.dct_global_param.get(param_name, None)

    def get_params(self, param_name=None):
        params = []
        for name in dir(self):
            var = getattr(self, name)
            if not isinstance(var, Param):
                continue
            if param_name:
                if var.get_name() == param_name:
                    return var
            else:
                params.append(var)
        return params

    def set_media_param(self, dct_media_param):
        self.dct_media_param = dct_media_param

    def get_media_param(self, param_name):
        return self.dct_media_param.get(param_name, None)

    def set_original_image(self, image):
        self.original_image = image

    def get_original_image(self):
        return self.original_image

    def notify_output_observers(self, data):
        for obs in self._output_observers:
            obs(data)

    def get_list_output_observer(self):
        return self._output_observers

    def add_output_observer(self, observer):
        self._output_observers.append(observer)

    def remove_output_observer(self, observer):
        self._output_observers.remove(observer)

    def get_media(self, name):
        from resource import Resource

        resource = Resource()
        return resource.get_media(name)
