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

def create_execute(cppfunc):
    """
    Create and return an "execute" method for the dynamically
    created class that wraps the c++ filters
    """
    def execute(self, image):
        notify = self.notify_output_observers
        cppfunc(image, notify)
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
        # this class herit of Filter
        Filter.__init__(self)
        self.params = {}
        cppfunc(self.params, self.py_init_param)
    return __init__