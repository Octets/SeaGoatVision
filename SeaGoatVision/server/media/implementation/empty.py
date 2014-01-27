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

from SeaGoatVision.server.media.media import Media
from SeaGoatVision.commons import keys
import numpy as np


class Empty(Media):

    """Do nothing"""

    def __init__(self, name):
        # Go into configuration/template_media for more information
        super(Empty, self).__init__()
        self.media_name = name
        print(name)
        self.image = np.zeros((1, 1), np.float32)

    def get_type_media(self):
        return keys.get_media_empty_name()

    def next(self):
        return self.image
