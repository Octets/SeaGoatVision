#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This filename is part of SeaGoatVision.
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

class Filter(object):
    def __init__(self):
        self._output_observers = list()
        self.original_image = None
        self.name = None
        self.lst_global_param = []

    def serialize(self):
        return {"filter_name":self.__class__.__name__, "lst_param":[param.serialize() for param in self.get_params()]}

    def deserialize(self, value):
        status = True
        for param_ser in value.get("lst_param"):
            param_name = param_ser.get("filter_name", None)
            if not param_name:
                # TODO: deprecated - name doesn't exist
                param_name = param_ser.get("name", None)
                if not param_name:
                    continue
            param = self.get_params(param_name=param_name)
            status &= param.deserialize(param_ser)
        return status

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def destroy(self):
        # It's called just before to be destroyed
        pass

    def configure(self):
        pass

    def set_global_params(self, lst_global_param):
        # complete the list and point on it
        for param in self.lst_global_param:
            lst_global_param.append(param)
        self.lst_global_param = lst_global_param[:]

    def get_global_params(self, param_name):
        for param in self.lst_global_param:
            if param.get_name() == param_name:
                return param
        return None

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
