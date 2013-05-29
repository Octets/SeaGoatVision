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

from SeaGoatVision.server.configuration.template_media.conf_webcam import Conf_webcam
from SeaGoatVision.server.configuration.template_media.conf_firewire import Conf_firewire

# keep always true for public configuration
# It's useful if you need to disable private config
active_configuration = True

## Networking
### Server tcp output notification
port_tcp_output = 8090


## Media
lst_media = []

# add camera webcam with default value
lst_media.append(Conf_webcam())


## Filterchain
show_public_filterchain = True


## Filter
show_public_filter = True

