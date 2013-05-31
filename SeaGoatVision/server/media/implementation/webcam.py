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

class Webcam(Media_streaming):
    """Return images from the webcam."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        self.config = config
        Media_streaming.__init__(self)
        self.run = True
        self.video = None
        video = cv2.VideoCapture(self.config.no)
        if video.isOpened():
            self.isOpened = True
            video.release()
        self.shape = (320, 240)

    def open(self):
        self.video = cv2.VideoCapture(self.config.no)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.shape[0])
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.shape[1])
        # call open when video is ready
        Media_streaming.open(self)

    def next(self):
        run, image = self.video.read()
        if run == False:
            raise StopIteration
        return image

    def close(self):
        Media_streaming.close(self)
        self.video.release()
