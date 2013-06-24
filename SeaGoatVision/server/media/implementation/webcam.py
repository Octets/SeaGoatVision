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
from SeaGoatVision.server.media.media_streaming import Media_streaming
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons.param import Param
import logging

logger = logging.getLogger("seagoat")

class Webcam(Media_streaming):
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
            self.isOpened = True
            video.release()
        self.actual_resolution_name = "800x600"
        self.dct_resolution = {self.actual_resolution_name:(800, 600),
                               "320x240":(320, 240),
                               "640x480":(640, 480),
                               "1024x768":(1024, 768),
                               "1280x960":(1280, 960)}
        self.actual_fps_name = "30"
        self.dct_fps = {self.actual_fps_name:30, "15":15, "7.5":7.5}

        self.deserialize(self.config.read_media(self.get_name()))

    def serialize(self):
        return {"resolution":self.actual_resolution_name, "fps":self.actual_fps_name}

    def deserialize(self, data):
        if not data:
            return False
        if type(data) is not dict:
            logger.error("Wrong format data, suppose to be dict into camera %s" % self.get_name())
            return False
        res = data.get("resolution", None)
        if res:
            self.change_resolution(res)
        res = data.get("fps", None)
        if res:
            self.change_fps(res)
        return True

    def open(self):
        try:
            shape = self.dct_resolution[self.actual_resolution_name]
            fps = self.dct_fps[self.actual_fps_name]

            self.video = cv2.VideoCapture(self.own_config.no)
            self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, shape[0])
            self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, shape[1])
            self.video.set(cv2.cv.CV_CAP_PROP_FPS, fps)
        except Exception as e:
            logger.error("Exception when open camera %s: %s", self.get_name(), e)
            return False
        # call open when video is ready
        return Media_streaming.open(self)

    def next(self):
        run, image = self.video.read()
        if run == False:
            raise StopIteration
        return image

    def close(self):
        Media_streaming.close(self)
        self.video.release()
        return True

    def change_resolution(self, resolution):
        """ Param: resolution type string, need to be a key of dct_resolution"""
        if resolution not in self.dct_resolution:
            logger.error("The key %s not in the list of resolution %s of media %s.",
                  resolution, self.dct_resolution.keys(), self.get_name())
            return False
        self.actual_resolution_name = resolution
        return self.reload()

    def change_fps(self, fps):
        """ Param: fps type string, need to be a key of dct_fps"""
        if fps not in self.dct_fps:
            logger.error("Error: The key %s not in the list of fps %s of media %s.",
                  resolution, self.dct_fps.keys(), self.get_name())
            return False
        self.actual_fps_name = fps
        return self.reload()

    def get_properties_param(self):
        resolution = Param("resolution", self.actual_resolution_name, lst_value=self.dct_resolution.keys())
        fps = Param("fps", self.actual_fps_name, lst_value=self.dct_fps.keys())
        return [resolution, fps]

    def update_property_param(self, param_name, value):
        if param_name == "resolution":
            return self.change_resolution(value)
        elif param_name == "fps":
            return self.change_fps(value)
        return False
