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

from SeaGoatVision.server.configuration.public import config as public_config
try:
    from SeaGoatVision.server.configuration.private import config as private_config
except:
    pass

class Configuration:
    # TODO do a singleton
    def __init__(self):
        self.public_config = public_config
        try:
            if private_config.active_configuration:
                self.private_config = private_config
            else:
                self.private_config = None
        except:
            self.private_config = None

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

