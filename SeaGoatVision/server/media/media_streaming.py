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

from media import Media
from SeaGoatVision.commons.keys import get_media_type_streaming_name
import time
import os
import cv2
import cv

class Media_streaming(Media):
    def is_media_streaming(self):
        return True

    def is_media_video(self):
        return False

    def get_type_media(self):
        return get_media_type_streaming_name()

    def start_record(self, path=None):
        # TODO manage multiple record
        # manage only one record at time
        if self.writer:
            self.stop_record()
        add_format_name = False
        name = ""
        if path:
            name = path
            if os.path.isdir(path):
                add_format_name = True
        else:
            add_format_name = True
        if add_format_name:
            name += "/%s.avi" % time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())

        fps = 8
        frame_size = (320, 240)
        # fourcc = cv.CV_FOURCC('D','I','V','X')
        # fourcc = cv.CV_FOURCC('V', 'P', '8', '0') # not work
        # fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
        # fourcc = cv.CV_FOURCC('D', 'I', 'B', ' ')  # Uncompressed RGB, 24 or 32 bit  - not working linux
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
