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
Description : Configuration manage configuration file.
"""
import os
import json

from SeaGoatVision.server.configuration.public import config as public_config
try:
    from SeaGoatVision.server.configuration.private import config as private_config
except:
    pass

class Configuration(object):
    _instance = None

    def __new__(cls):
        # Singleton
        if not cls._instance:
            # first instance
            cls.public_config = public_config
            try:
                if private_config.active_configuration:
                    cls.private_config = private_config
                else:
                    cls.private_config = None
            except:
                cls.private_config = None

            # instance class
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self.get_is_show_public_filterchain():
            self.dir_filterchain = "SeaGoatVision/server/configuration/public/filterchain/"
        else:
            self.dir_filterchain = "SeaGoatVision/server/configuration/private/filterchain/"
        self.extFilterChain = ".filterchain"

    #### General config
    def get_tcp_output_config(self):
        if self.private_config:
            try:
                return self.private_config.port_tcp_output
            except:
                return self.public_config.port_tcp_output
        return self.public_config.port_tcp_output

    def get_lst_media_config(self):
        if self.private_config:
            try:
                return self.private_config.lst_media
            except:
                return self.public_config.lst_media
        return self.public_config.lst_media

    def get_is_show_public_filterchain(self):
        if self.private_config:
            try:
                return self.private_config.show_public_filterchain
            except:
                return self.public_config.show_public_filterchain
        return self.public_config.show_public_filterchain

    def get_is_show_public_filter(self):
        if self.private_config:
            try:
                return self.private_config.show_public_filter
            except:
                return self.public_config.show_public_filter
        return self.public_config.show_public_filter

    #### Filterchain
    def list_filterchain(self):
        if not os.path.isdir(self.dir_filterchain):
            return []
        return [files[:-len(self.extFilterChain)] for files in os.listdir(self.dir_filterchain) if files.endswith(self.extFilterChain)]

    def read_filterchain(self, filterchain_name):
        file_name = self._get_filterchain_filename(filterchain_name)
        f = open(file_name, "r")
        if not f:
            print("Error, file not exist or other reason : %s" % file_name)
            return None
        str_value = f.readlines()
        try:
            value = json.loads("".join(str_value))
        except:
            print("Error, the file %s not contain json data." % file_name)
            value = None
        f.close()
        return value

    def write_filterchain(self, filterchain):
        file_name = self._get_filterchain_filename(filterchain.get_name())
        f = open(file_name, "w")
        if not f:
            return False
        str_value = json.dumps(filterchain.serialize(), indent=4)
        f.write(str_value)
        f.close()
        return True

    def delete_filterchain(self, filterchain_name):
        file_name = self._get_filterchain_filename(filterchain_name)
        try:
            return os.remove(file_name)
        except OSError:
            return False

    def _get_filterchain_filename(self, filterchain_name):
        return "%s%s%s" % (self.dir_filterchain, filterchain_name, self.extFilterChain)
