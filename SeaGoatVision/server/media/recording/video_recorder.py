#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This filename is part of SeaGoatVision.
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

import cv
import cv2
import os
import time
import logging
from SeaGoatVision.server.core.configuration import Configuration

logger = logging.getLogger("seagoat")

class Video_recorder:
    def __init__(self, media):
        self.writer = None
        self.media = media
        self.config = Configuration()
        self.file_name = None

    def start(self, shape, path=None, fps=30):
        # TODO manage multiple record
        # manage only one record at time
        if self.writer:
            self.stop()
        add_format_name = False
        if path:
            # exception, if not contain /, maybe it's just a filename
            if "/" not in path:
                name = "%s%s.avi" % (self.config.get_path_save_record(), path)
            else:
                # TODO need to add extension when giving all path with filename?
                name = path
                if os.path.isdir(path):
                    add_format_name = True
        else:
            add_format_name = True
            # TODO mkdir if directory
            name =  self.config.get_path_save_record()
        if add_format_name:
            name += "%s.avi" % time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())

        if not os.path.isfile(name):
            logger.error("Record: file already exist %s", name)
            return

        self.file_name = name
        logger.info("Start record on path: %s", name)

        fps = 8
        # fourcc = cv.CV_FOURCC('D','I','V','X')
        # fourcc = cv.CV_FOURCC('F', 'L', 'V', '1')
        # fourcc = cv.CV_FOURCC('V', 'P', '8', '0') # not work
        # fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
        # fourcc = cv.CV_FOURCC('D', 'I', 'B', ' ')  # Uncompressed RGB, 24 or 32 bit  - not working linux
        fourcc = cv.CV_FOURCC('I', 'Y', 'U', 'V')  # Uncompressed YUV, 4:2:0 chroma subsampled , same of 'I420'
        self.writer = cv2.VideoWriter(filename=name, fourcc=fourcc, fps=fps, frameSize=shape, isColor=1)
        self.writer.open(name, fourcc, fps, shape, 1)
        self.media.add_observer(self.writer.write)
        return True

    def get_file_name(self):
        if not self.file_name:
            return ""
        return self.file_name

    def stop(self):
        self.file_name = None
        if not self.writer:
            return False
        self.media.remove_observer(self.writer.write)
        del self.writer
        self.writer = None
        return True
