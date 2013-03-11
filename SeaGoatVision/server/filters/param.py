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
Filter must not modify Param.
Different type :
 - INT : integer. Can have min or max value. Can use table of specific value.
 - FLOAT : float. Same of INT, but use float.
 - BOOL : boolean. Only True or False.

TIPS :
 - You want only EVEN number for your gaussian blur?
    lst_gauss_value = [i for i in range(100) if not(i % 2)]
    kern_gauss_blur = Param("kern_gauss_blur", 4, lst_value=lst_gauss_value)
 - In this example, we can't access to -1 because of min.
    p = Param("f", 2, min_v=1, max_v=19, lst_value=[-1,2,4,6,10])
 - We can use a threshold value. In this situation, we have two value.
  The value is always the low value and the threshold_hight is the hight value.
    p = Param("f", 2, min_v=1, max_v=8, threshold_hight=5)
"""
class Param(object):
    """Let type_t to None to use autodetect.
    type_t need to be a <type>

    Param manager type : bool, int and float
    """
    def __init__(self, name, value, min_v=None, max_v=None, lst_value=None,\
                type_t=None, threshold_hight=None):
        if type(name) is not str:
            raise Exception("Name must be string value.")
        self.name = name
        self.min_v = None
        self.max_v = None
        self.value = None
        self.default_value = None
        self.type_t = None
        self.threshold_hight = None
        self._valid_param(value, min_v, max_v, lst_value, type_t, \
                threshold_hight)
        self.set(value)
        self.default_value = self.value

    def _valid_param(self, value, min_v, max_v, lst_value, type_t, \
                threshold_hight):
        type_v = type(value)
        if type_t is not None and type(type_t) is not type:
            raise Exception("Wrong type of type_t : %s" % type(self.type_t))
        else:
            type_t = type_v
        if not(type_v is int or type_v is bool or type_v is float):
            raise Exception("Param don't manage type %s" % type_v)
        if type_v is float or type_v is int:
            # check min and max
            if min_v is not None and \
                not(type(min_v) is float or type(min_v) is int):
                raise Exception("min_v must be float or int.")
            if max_v is not None and \
                    not(type(max_v) is float or type(max_v) is int):
                raise Exception("max_v must be float or int.")
            if lst_value is not None and \
                    not(type(lst_value) is tuple or type(lst_value) is list):
                raise Exception("lst_value must be list or tuple")
            if type_v is float:
                min_v = None if min_v is None else float(min_v)
                max_v = None if max_v is None else float(max_v)
                lst_value = None if lst_value is None else \
                            [float(value) for value in lst_value]
            if type_v is int:
                min_v = None if min_v is None else int(min_v)
                max_v = None if max_v is None else int(max_v)
                lst_value = None if lst_value is None else \
                            [int(value) for value in lst_value]
        self.min_v = min_v
        self.max_v = max_v
        self.lst_value = lst_value
        self.type_t = type_t
        self.thres_h = threshold_hight

    def reset(self):
        self.value = self.default_value

    def get_name(self):
        return self.name

    def get_min(self):
        return self.min_v

    def get_max(self):
        return self.max_v

    def get(self):
        if self.thres_h is not None:
            return (self.value, self.thres_h)
        return self.value

    def set(self, value, thres_hight=None):
        if type(value) is not self.type_t:
            raise Exception("value is wrong type. Expected %s and receive %s" \
                    % (self.type_t, type(value)))
        if self.type_t is int or self.type_t is float:
            if self.min_v is not None and value < self.min_v:
                raise Exception("Value %s is lower then min %s" % \
                    (value, self.min_v))
            if self.max_v is not None and value > self.max_v:
                raise Exception("Value %s is upper then max %s" % \
                    (value, self.max_v))
            if self.lst_value is not None and value not in self.lst_value:
                raise Exception("value %s is not in lst of value" % (value))
        if self.thres_h is not None:
            if thres_hight is None:
                if value > self.thres_h:
                    msg = "Threshold bot %s is upper then threshold top %s." \
                           % (value, self.thres_h)
                    raise Exception(msg)
            else:
                if type(thres_hight) is not self.type_t:
                    msg = "value is wrong type. Expected %s and receive %s" \
                        % (self.type_t, type(value))
                    raise Exception(msg)
                elif value > thres_hight:
                    msg = "Threshold low %s is upper then threshold hight %s." \
                           % (value, thres_hight)
                    raise Exception(msg)
                if thres_hight > self.max_v:
                    raise Exception("Threshold hight %s is upper then max %s." \
                            % (thres_hight, self.max_v))
                self.thres_h = thres_hight
        self.value = value

    def get_type(self):
        return self.type_t
