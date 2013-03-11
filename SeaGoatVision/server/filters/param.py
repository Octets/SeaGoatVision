#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of SeaGoatVision.
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
"""
Parameter is used by filter and client. This is public variable with specific
type of filter.
Different type :
 - INT : integer. Can have min or max value. Can use table of specific value.
 - FLOAT : float. Same of INT, but use float.
 - BOOL : boolean. Only True or False.

TIPS :
 - You want only EVEN number for your gaussian blur?
    lst_gauss_value = [i for i in range(100) if not(i % 2)]
    kern_gauss_blur = Parameter("kern_gauss_blur", 4,\
            lst_value=lst_gauss_value)
"""
class Param(object):
    INT, FLOAT, BOOL = range(3)

    def __init__(self, name, value, min_v=None, max_v=None, type_t=INT,\
                lst_value=None):
        if type(name) is not str:
            raise Exception("Parameter : name must be string value.")
        self.name = name
        self.min_v = min_v
        self.max_v = max_v
        self.value = None
        self.default_value = None
        # check type
        if self.INT > type_t or self.BOOL < type_t:
            raise Exception("Parameter : Wrong type.")
        self.type_t = type_t
        self.set_value(value)
        self.default_value = self.value

    def reset(self):
        self.value = self.default_value

    def get_name(self):
        return self.name

    def get_min(self):
        return self.min_v

    def get_max(self):
        return self.max_v

    def get_value(self):
        return self.value

    def set_value(self, value):
        if self.type_t == self.INT:
            self.value = int(value)

    def get_type(self):
        return self.type_t
