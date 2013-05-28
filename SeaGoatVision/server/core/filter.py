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

    def configure(self):
        pass

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
