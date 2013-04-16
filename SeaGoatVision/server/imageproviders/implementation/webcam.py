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
import cv
from time import gmtime, strftime

class Webcam(object):
    """Return images from the webcam."""

    def __init__(self):
        self.writer = None
        self.run = True
        self.camera_number = 0
        self.video = cv2.VideoCapture(self.camera_number)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    def __iter__(self):
        return self

    def start_record(self):
        # manage only one record at time
        if self.writer:
            self.stop_record()
        name = "%s.avi" % strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        fps = 8
        frame_size = (320, 240)
        # fourcc = cv.CV_FOURCC('D','I','V','X')
        # fourcc = cv.CV_FOURCC('V', 'P', '8', '0') # not work
        # fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
        #fourcc = cv.CV_FOURCC('D', 'I', 'B', ' ')  # Uncompressed RGB, 24 or 32 bit  - not working linux
        fourcc = cv.CV_FOURCC('I', 'Y', 'U', 'V')  # Uncompressed YUV, 4:2:0 chroma subsampled , same of 'I420'
        self.writer = cv2.VideoWriter(filename=name, fourcc=fourcc, fps=fps, frameSize=frame_size, isColor=1)
        self.writer.open(name, fourcc, fps, frame_size, 1)
        return True

    def stop_record(self):
        if not self.writer:
            return False
        del self.writer
        self.writer = None
        return True

    def next(self):
        run, image = self.video.read()
        if run == False:
            raise StopIteration
        if self.writer:
            self.writer.write(image)
        return image

    def close(self):
        self.video.release()
