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
import video1394
import numpy as np
import Image

class Firewire(Media_streaming):
    """Return images from the webcam."""

    def __init__(self):
        self.camera = None
        Media_streaming.__init__(self)
        self.is_rgb = True

    def open(self):
        self.ctx = video1394.DC1394Context()
        camera = self.ctx.createCamera(0)
        camera.resetBus()
        if self.is_rgb:
            camera.mode = video1394.VIDEO_MODE_800x600_RGB8
        else:
            camera.mode = video1394.VIDEO_MODE_800x600_YUV422
        camera.framerate = video1394.FRAMERATE_15
        camera.isoSpeed = video1394.ISO_SPEED_400
        self.camera = camera
        self.camera.start()
        self.camera.grabEvent.addObserver(self.camera_observer)
        # call open when video is ready
        Media_streaming.open(self)

    def camera_observer(self, im, timestamp):
        if self.is_rgb:
            image = Image.fromarray(im, "RGB")
            image2 = np.asarray(image, dtype="uint8")
        else:
            image2 = im
        #shape = (im.shape[0], im.shape[1], 3)
        #rgb = np.zeros(shape, dtype=np.uint8)
        #np.copyto(rgb, im, casting="no")
        self.notify_observer(image2)

    def next(self):
        pass

    def close(self):
        Media_streaming.close(self)
        self.camera.stop()
