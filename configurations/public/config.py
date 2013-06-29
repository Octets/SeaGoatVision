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

# This file contain configuration about server.py

import datetime
from configurations.template_media.conf_webcam import Conf_webcam
from configurations.template_media.conf_firewire import Conf_firewire

# keep always true for public configuration
# It's useful if you need to disable private config
active_configuration = True

## Log
# no log When log_path is None else put a string path with file_name
log_path = None
# exemple of log_path
#log_path = "/tmp/log_%s.log" % datetime.datetime.now().strftime("%Y-%m-%d_%I:%M:%S")

## Networking
### Server tcp output notification
port_tcp_output = 8090


## Media
path_save_record = "" # empty string will record on root of seagoat project
lst_media = []

# add camera webcam with default value
cam = Conf_webcam()
lst_media.append(cam)


## Filterchain
show_public_filterchain = True


## Filter
show_public_filter = True

