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

try:
    from thirdparty.public.pydc1394 import video1394
except:
    pass
from SeaGoatVision.server.media.implementation.firewire import Firewire

class Conf_firewire:
    def __init__(self):
        self.media = Firewire
        self.name = "Firewire"
        self.no = -1
        self.default_fps = None

        # specific for firewire device
        self.guid = None
        try:
            self.iso_speed = video1394.ISO_SPEED_400
            self.mode = video1394.VIDEO_MODE_800x600_YUV422
            self.framerate = video1394.FRAMERATE_15
            self.is_rgb = False
            self.is_format7 = False
            self.is_mono = False
            self.is_yuv = True
        except:
            pass
