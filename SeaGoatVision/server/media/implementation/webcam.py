#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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
from SeaGoatVision.server.media.media_streaming import MediaStreaming
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class Webcam(MediaStreaming):
    """Return images from the webcam."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        self.config = Configuration()
        self.own_config = config
        super(Webcam, self).__init__()
        self.media_name = config.name
        self.run = True
        self.video = None
        video = cv2.VideoCapture(config.no)
        if video.isOpened():
            self._is_opened = True
            video.release()

        self._create_params()

        self.deserialize(self.config.read_media(self.get_name()))

    def _create_params(self):
        self.dct_params = {}

        default_resolution_name = "800x600"
        self.dct_resolution = {default_resolution_name: (800, 600),
                               "320x240": (320, 240),
                               "640x480": (640, 480),
                               "1024x768": (1024, 768),
                               "1280x960": (1280, 960),
                               "1280x1024": (1280, 1024)}
        self.param_resolution = Param(
            "resolution",
            default_resolution_name,
            lst_value=self.dct_resolution.keys())
        self.param_resolution.add_notify(self.reload)

        default_fps_name = "30"
        self.dct_fps = {default_fps_name: 30, "15": 15, "7.5": 7.5}
        self.param_fps = Param("fps", default_fps_name,
                               lst_value=self.dct_fps.keys())
        self.param_fps.add_notify(self.reload)

    def open(self):
        try:
            shape = self.dct_resolution[self.param_resolution.get()]
            fps = self.dct_fps[self.param_fps.get()]

            # TODO check argument video capture
            self.video = cv2.VideoCapture(self.own_config.no)
            self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, shape[0])
            self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, shape[1])
            self.video.set(cv2.cv.CV_CAP_PROP_FPS, fps)
        except BaseException as e:
            log.printerror_stacktrace(
                logger, "Open camera %s: %s" %
                (self.get_name(), e))
            return False
        # call open when video is ready
        return MediaStreaming.open(self)

    def next(self):
        run, image = self.video.read()
        if not run:
            raise StopIteration
        return image

    def close(self):
        MediaStreaming.close(self)
        self.video.release()
        self._is_opened = False
        return True
