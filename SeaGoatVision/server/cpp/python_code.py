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

from SeaGoatVision.server.core.filter import Filter
from SeaGoatVision.commons.param import Param


def create_execute(cppfunc):
    """
    Create and return an "execute" method for the dynamically
    created class that wraps the c++ filters
    """

    def execute(self, image):
        cppfunc(image)
        return image
    return execute


def create_configure(cppfunc):
    """
    """

    def configure(self):
        cppfunc()
    return configure


def create_init(cppfunc, params):
    """
    """

    def __init__(self):
        # this subclass of Filter
        Filter.__init__(self)
        self.params = {}
        cppfunc(
            self.params,
            self.py_init_param,
            self.notify_output_observers,
            self.dct_global_param,
            self.py_init_global_param)
    return __init__


def create_destroy(cppfunc):
    """
    Just call the destructor
    """

    def destroy(self):
        cppfunc()
    return destroy


def create_set_original_image(cppfunc):
    def set_original_image(self, image_original):
        cppfunc(image_original)
    return set_original_image


def create_set_global_params(cppfunc):
    def set_global_params(self, dct_global_param):
        self.dct_global_param = dct_global_param
        cppfunc(dct_global_param)
    return set_global_params


def py_init_global_param(self, name, value, min=None, max=None):
    param = Param(name, value, min_v=min, max_v=max)
    self.dct_global_param[name] = param


def py_init_param(self, name, value, min=None, max=None):
    param = Param(name, value, min_v=min, max_v=max)
    self.params[name] = param
    setattr(self, name, param)
