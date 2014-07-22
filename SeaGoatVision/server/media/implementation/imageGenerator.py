#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
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

from SeaGoatVision.server.media.media_streaming import MediaStreaming
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import log
import numpy as np

logger = log.get_logger(__name__)


class ImageGenerator(MediaStreaming):
    """Return a generate image."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        self.config = Configuration()
        self.own_config = config
        super(ImageGenerator, self).__init__()
        self.media_name = config.name
        self.run = True
        self._is_opened = True

        self._create_params()

        self.deserialize(self.config.read_media(self.get_name()))

    def _create_params(self):
        default_width = 800
        self.param_width = Param("width", default_width, min_v=1, max_v=1200)
        self.param_width.add_group("Resolution")
        self.param_width.set_description("Change width resolution.")

        default_height = 600
        self.param_height = Param("height", default_height, min_v=1,
                                  max_v=1200)
        self.param_height.add_group("Resolution")
        self.param_height.set_description("Change height resolution.")

        default_fps = 30
        self.param_fps = Param("fps", default_fps, min_v=1, max_v=100)
        self.param_fps.set_description("Change frame per second.")

        self.param_color_r = Param("color_r", 0, min_v=0, max_v=255)
        self.param_color_r.add_group("Color")
        self.param_color_r.set_description("Change red color.")

        self.param_color_g = Param("color_g", 0, min_v=0, max_v=255)
        self.param_color_g.add_group("Color")
        self.param_color_g.set_description("Change green color.")

        self.param_color_b = Param("color_b", 0, min_v=0, max_v=255)
        self.param_color_b.add_group("Color")
        self.param_color_b.set_description("Change blue color.")

        self.param_auto_color = Param("auto-change-color", False)
        self.param_auto_color.set_description(
            "Change the color automatically.")
        self.param_auto_color.add_group("Color")

        self.param_transpose_r_color = Param("Transpose red color", None)
        self.param_transpose_r_color.set_description(
            "Copy the red color on others color.")
        self.param_transpose_r_color.add_notify(self._transpose_red_color)
        self.param_transpose_r_color.add_group("Color")

        self.param_freeze = Param("freeze", False)
        self.param_freeze.set_description("Freeze the stream.")

    def next(self):
        if self.param_freeze.get():
            return

        width = self.param_width.get()
        height = self.param_height.get()
        color_r = self.param_color_r.get()
        color_g = self.param_color_g.get()
        color_b = self.param_color_b.get()

        if self.param_auto_color.get():
            color_r += 1
            if color_r > 255:
                color_r = 0
            color_g += 2
            if color_g > 255:
                color_g = 0
            color_b += 3
            if color_b > 255:
                color_b = 0

            self.param_color_r.set(color_r)
            self.param_color_r.set_lock(True)
            self.param_color_g.set(color_g)
            self.param_color_g.set_lock(True)
            self.param_color_b.set(color_b)
            self.param_color_b.set_lock(True)
        else:
            self.param_color_r.set_lock(False)
            self.param_color_g.set_lock(False)
            self.param_color_b.set_lock(False)

        image = np.zeros((height, width, 3), dtype=np.uint8)

        image[:, :, 0] += color_b
        image[:, :, 1] += color_g
        image[:, :, 2] += color_r
        return image

    def _transpose_red_color(self, param):
        color_r = self.param_color_r.get()
        self.param_color_g.set(color_r)
        self.param_color_b.set(color_r)
