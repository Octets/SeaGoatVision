#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
#
# SeaGoatVision is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Shared parameter is used by filter in intern only.

"""
import numpy as np
from SeaGoatVision.commons import log
from . import param

logger = log.get_logger(__name__)


class SharedParam(object, param.Param):
    """Like Param
    Shared Param manager type : None, ndarray, unicode, bool, str, int, long
    and float
    """

    def __init__(self, name, value, min_v=None, max_v=None, lst_value=None,
                 force_type=None, thres_h=None, serialize=None):
        super(SharedParam, self).__init__(name, value, min_v=min_v,
                                          max_v=max_v, lst_value=lst_value,
                                          force_type=force_type,
                                          thres_h=thres_h, serialize=serialize)

    def _valid_param(self, value, min_v, max_v, lst_value, threshold):
        super(SharedParam, self)._valid_param(value, min_v, max_v, lst_value,
                                              threshold, type_validated=True)
        type_t = type(value)
        if type_t is not np.ndarray:
            raise ValueError("Param don't manage type %s" % type_t)

    def get(self):
        # Exception, cannot convert to numpy array
        # this can create bug in your filter if you pass wrong type
        if self.force_type is np.ndarray:
            return self.value
        return super(SharedParam, self).get()
