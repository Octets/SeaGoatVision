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

import cv2
from cv2 import cv
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter

# This filter is created to test communication in Seagoat with unit test


class TestSeagoat(Filter):

    def __init__(self):
        Filter.__init__(self)
        self.param_str = Param("param_str", "")

    def configure(self):
        # This is called when param is modify
        pass

    def execute(self, image):
        self.notify_output_observers(self.param_str.get())
        return image
