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
"""
Description : contain shared variable inter-widget and signal connect with interrupt
"""


class SharedInfo(object):
    _instance = None

    def __new__(cls):
        # Singleton
        if not cls._instance:
            # first instance
            # list of shared variable
            cls.dct_variable = {}
            cls.dct_variable["media"] = None
            cls.dct_variable["filterchain"] = None
            cls.dct_variable["filter"] = None
            cls.dct_variable["execution"] = None
            cls.dct_variable["close_exec"] = None
            cls.dct_variable["filterchain_edit_mode"] = None
            cls.dct_variable["path_media"] = None
            cls.dct_variable["start_execution"] = None

            cls.dct_signal = {}
            for key in cls.dct_variable.keys():
                cls.dct_signal[key] = []

            # instance class
            cls._instance = super(SharedInfo, cls).__new__(cls)
        return cls._instance

    def connect(self, key, callback):
        if key not in self.dct_signal:
            return False
        lst_callback = self.dct_signal[key]
        if callback in lst_callback:
            return False
        lst_callback.append(callback)
        # call if already contain value
        value = self.dct_variable.get(key, None)
        if value is not None:
            callback(value)
        return True

    def get(self, key):
        return self.dct_variable.get(key, None)

    def set(self, key, value):
        if key not in self.dct_variable:
            return False
        self.dct_variable[key] = value
        for callback in self.dct_signal[key]:
            callback(value)
        return True
