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
Parameter is used by filter and client. This is public variable with specific
type of filter.
Filter must not modify Param.
Different type :
 - INT : integer. Can have min or max value. Can use table of specific value.
 - FLOAT : float. Same of INT, but use float.
 - BOOL : boolean. Only True or False.
 - STRING : string.

TIPS :
 - You want only EVEN number for your gaussian blur?
    lst_gauss_value = [i for i in range(100) if not(i % 2)]
    kern_gauss_blur = Param("kern_gauss_blur", 4, lst_value=lst_gauss_value)
 - In this example, we can't access to -1 because of min.
    p = Param("f", 2, min_v=1, max_v=19, lst_value=[-1,2,4,6,10])
 - We can use a threshold value. In this situation, we have two value.
  The value is always the low value and the threshold_high is the high value.
    p = Param("f", 2, min_v=1, max_v=8, threshold=5)
 - When value is None, you can use it like a trigger.
"""
from SeaGoatVision.commons import log
import types

logger = log.get_logger(__name__)


class Param(object):
    """Param autodetect basic type
    force_type need to be a <type>
    If you want specific type, cast it to basic type and use force_type
    Param manager type : None, unicode, bool, str, int, long and float
    """

    def __init__(self, name, value, min_v=None, max_v=None, lst_value=None,
                 force_type=None, thres_h=None, serialize=None, is_lock=False):
        # constant float
        self.delta_float = 0.0001
        # Exception, can serialize
        self.lst_notify = []
        self.name = name
        self.lst_value = None
        self.min_v = None
        self.max_v = None
        self.value = None
        self.default_value = None
        self.type_t = None
        self.threshold = None
        self.force_type = None
        self.last_saved_value = None
        self.description = None
        self.first_initialize = True
        self._is_lock = is_lock
        self.lst_group = set()

        if serialize:
            status = self.deserialize(serialize)
            if not status:
                msg = "Wrong deserialize parameter, can't know the name - "
                "%s." % serialize
                raise ValueError(msg)
            # logger.debug("Param %s deserialization complete, value %s" % (
            #    self.name, self.value))
            return

        if not isinstance(name, str) and not isinstance(name, unicode):
            raise ValueError("Name must be string value.")

        self._init_param(value, min_v, max_v, lst_value, force_type, thres_h,
                         is_lock)

    def _init_param(self, value, min_v, max_v, lst_value, force_type,
                    threshold, is_lock):
        self._valid_param(value, min_v, max_v, lst_value, threshold)
        self._is_lock = is_lock
        self.set(value)
        self.last_saved_value = self.value
        if self.first_initialize:
            self.default_value = self.value
        if force_type:
            self.force_type = force_type
        else:
            self.force_type = self.type_t
        self.first_initialize = False

    def _valid_param(self, value, min_v, max_v, lst_value, threshold,
                     type_validated=False):
        type_t = type(value)
        if not type_validated and not (type_t is int
                                       or type_t is types.NoneType
                                       or type_t is bool
                                       or type_t is float
                                       or type_t is str
                                       or type_t is long
                                       or type_t is unicode):
            raise ValueError("Param don't manage type %s" % type_t)
        if type_t is unicode:
            type_t = str
        if type_t is long:
            type_t = int
            if min_v is not None:
                min_v = int(min_v)
            if max_v is not None:
                max_v = int(max_v)
        if type_t is float or type_t is int:
            # check min and max
            if min_v is not None:
                type_min = type(min_v)
                if not (type_min is float
                        or type_min is int
                        or type_min is long):
                    raise ValueError(
                        "min_v must be float or int, type is %s." % type_min)
            if max_v is not None:
                type_max = type(max_v)
                if not (type_max is float
                        or type_max is int
                        or type_max is long):
                    raise ValueError(
                        "max_v must be float or int, type is %s." % type(
                            max_v))
            if type_t is float:
                min_v = None if min_v is None else float(min_v)
                max_v = None if max_v is None else float(max_v)
                lst_value = None if lst_value is None else [float(value) for
                                                            value in lst_value]
            if type_t is int:
                min_v = None if min_v is None else int(min_v)
                max_v = None if max_v is None else int(max_v)
                lst_value = None if lst_value is None else [int(value) for
                                                            value
                                                            in lst_value]
        if lst_value is not None and \
                not (isinstance(lst_value, tuple) or isinstance(lst_value,
                                                                list)):
            raise ValueError(
                "lst_value must be list or tuple, type is %s." % type(
                    lst_value))
        self.min_v = min_v
        self.max_v = max_v
        self.lst_value = lst_value
        self.type_t = type_t
        self.threshold = threshold

    def serialize(self, is_config=False):
        if is_config:
            self.last_saved_value = self.value
        # Force_type is not supported
        ser = {
            "name": self.name,
            "value": self.value,
            "min_v": self.min_v,
            "max_v": self.max_v,
            "lst_value": self.lst_value,
            "threshold": self.threshold,
            "is_lock": self._is_lock,
        }
        if not is_config:
            ser["description"] = self.description
            ser["lst_group"] = list(self.lst_group)
        return ser

    def deserialize(self, value):
        if not isinstance(value, dict):
            return False
        name = value.get("name", None)
        if not name:
            return False
        self.name = name
        self._init_param(
            value.get("value", None),
            value.get("min_v", None),
            value.get("max_v", None),
            value.get("lst_value", None),
            value.get("force_type", None),
            value.get("threshold", None),
            value.get("is_lock", None),
        )

        description = value.get("description", None)
        if description:
            self.description = description
        lst_group = value.get("lst_group", None)
        if lst_group:
            self.lst_group = lst_group
        return True

    def reset(self):
        if self.value == self.last_saved_value:
            return
        self.value = self.last_saved_value
        self._send_notification()

    def set_as_default(self):
        if self.value == self.default_value:
            return
        self.value = self.default_value
        self._send_notification()

    def merge(self, param):
        self.name = param.name
        self.value = param.value
        self.min_v = param.min_v
        self.max_v = param.max_v
        self.lst_value = param.lst_value
        self.threshold = param.threshold

    def get_name(self):
        return self.name

    def get_min(self):
        return self.min_v

    def get_max(self):
        return self.max_v

    def get_list_value(self):
        if not self.lst_value:
            return
        return self.lst_value

    def add_notify(self, callback):
        # notify when set the value
        # pass the value in argument
        if callback in self.lst_notify:
            logger.warning("Already in notify %s" % self.get_name())
            return
        self.lst_notify.append(callback)

    def remove_notify(self, callback):
        if callback not in self.lst_notify:
            logger.warning("The callback wasn't in the list of notify "
                           "%s" % self.get_name())
            return
        self.lst_notify.remove(callback)

    def get(self):
        # Exception, cannot convert to numpy array
        # this can create bug in your filter if you pass wrong type
        if self.force_type is types.NoneType:
            return self.value
        if self.threshold is not None:
            return self.force_type(self.value), self.force_type(self.threshold)
        return self.force_type(self.value)

    def get_pos_list(self):
        if not self.lst_value:
            return -1
        return self.lst_value.index(self.get())

    def set(self, value, threshold=None):
        # don't change value if it's the same value, except for None
        if type(value) is not None:
            if value == self.value:
                return False
        if isinstance(value, unicode):
            value = str(value)
        if self.type_t is bool:
            value = bool(value)

        if self.type_t is int and (isinstance(value, float)
                                   or isinstance(value, long)):
            value = int(value)
        if self.type_t is float and isinstance(value, int):
            value = float(value)
        if not isinstance(value, self.type_t):
            raise ValueError(
                "value is wrong type. Expected %s and receive %s" % (
                    self.type_t, type(value)))
        self._validate_number(value)
        self._validate_threshold(value, threshold)
        # check if item is in list
        if self.lst_value and value not in self.lst_value:
            raise ValueError("The value %s is not in lst_value %s." % (
                value, self.lst_value))
        self.value = value
        # send the value on all notify callback
        self._send_notification()
        return True

    def _validate_number(self, value):
        if not (self.type_t is int or self.type_t is float):
            return
        delta_val = self.min_v - self.delta_float
        if self.min_v is not None and value < delta_val:
            msg = "Value %s is lower then min %s" % (value, self.min_v)
            raise ValueError(msg)
        delta_val = self.max_v + self.delta_float
        if self.max_v is not None and value > delta_val:
            msg = "Value %s is upper then max %s" % (value, self.max_v)
            raise ValueError(msg)
        if self.lst_value is not None and value not in self.lst_value:
            raise ValueError("value %s is not in lst of value" % value)

    def _validate_threshold(self, value, threshold):
        if self.threshold is None:
            return
        if threshold is None:
            if value > self.threshold:
                msg = "Threshold bot %s is upper then threshold top %s." % (
                    value, self.threshold)
                raise ValueError(msg)
            return
        if self.type_t is int and isinstance(threshold, float):
            threshold = int(threshold)
        if self.type_t is float and isinstance(threshold, int):
            threshold = float(threshold)
        if not isinstance(threshold, self.type_t):
            msg = "value is wrong type. Expected %s and receive %s" % (
                self.type_t, type(threshold))
            raise ValueError(msg)
        elif value > threshold:
            msg = "Threshold low %s is upper then threshold high %s." % (
                value, threshold)
            raise ValueError(msg)
        if threshold > self.max_v:
            msg = "Threshold high %s is upper then max %s." % (
                threshold, self.max_v)
            raise ValueError(msg)
        self.threshold = threshold

    def _send_notification(self):
        for notify in self.lst_notify:
            notify(self)

    def get_type(self):
        return self.force_type

    def set_description(self, description):
        # description provide in the code
        self.description = description

    def get_description(self):
        return self.description

    def add_group(self, group_name):
        # group is configured from filter
        self.lst_group.add(group_name)

    def get_groups(self):
        return list(self.lst_group)

    def lock(self):
        self.set_lock(True)

    def unlock(self):
        self.set_lock(False)

    def set_lock(self, is_lock):
        self._is_lock = is_lock
        self._send_notification()

    def get_is_lock(self):
        return self._is_lock
