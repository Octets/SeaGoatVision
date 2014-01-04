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

from SeaGoatVision.server.media.media_streaming import Media_streaming
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import log
import numpy as np

logger = log.get_logger(__name__)


class ImageGenerator(Media_streaming):

    """Return a generate image."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        self.config = Configuration()
        self.own_config = config
        super(ImageGenerator, self).__init__()
        self.media_name = config.name
        self.run = True
        self.image = None
        self.isOpened = True

        self._create_params()

        self.deserialize(self.config.read_media(self.get_name()))

    def _create_params(self):
        self.dct_params = {}

        default_width = 800
        param = Param("width", default_width, min_v=1, max_v=1200)
        self.dct_params["width"] = param

        default_height = 600
        param = Param("height", default_height, min_v=1, max_v=1200)
        self.dct_params["height"] = param

        default_fps = 30
        param = Param("fps", default_fps, min_v=1, max_v=100)
        self.dct_params["fps"] = param

    def serialize(self):
        return {"width": self.dct_params.get("width").get(), "height": self.dct_params.get("height"), "fps": self.dct_params.get("fps").get()}

    def deserialize(self, data):
        if not data:
            return False
        if not isinstance(data, dict):
            log.print_function(
                logger.error, "Wrong format data, suppose to be dict into camera %s" %
                self.get_name())
            return False
        res = data.get("width", None)
        if res:
            self.dct_params.get("width").set(res)
        res = data.get("height", None)
        if res:
            self.dct_params.get("height").set(res)
        res = data.get("fps", None)
        if res:
            self.dct_params.get("fps").set(res)
        return True

    def next(self):
        width = self.dct_params.get("width").get()
        height = self.dct_params.get("height").get()
        self.image = np.zeros((height, width, 3), dtype=np.uint8)
        return self.image

    def get_properties_param(self):
        return self.dct_params.values()

    def update_property_param(self, param_name, value):
        param = self.dct_params.get(param_name, None)
        if not param:
            return False
        param_value = param.get()
        if value == param_value:
            return True
        param.set(value)
        return True
