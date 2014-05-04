#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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

import os
import time
from PIL import Image
import cv2
from cv2 import cv
import numpy as np
from threading import Semaphore
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons import log
from subprocess import Popen, PIPE

logger = log.get_logger(__name__)


class VideoRecorder:
    def __init__(self, media):
        self.writer = None
        self.media = media
        self.config = Configuration()
        self.file_name = None
        self.process = None
        # create a semaphore to protect when closing ffmpeg
        self.sem = Semaphore(1)

    def start(self, shape, path=None, fps=30, compress=0):
        # TODO manage multiple record
        # manage only one record at time
        if self.process:
            self.stop()
        add_format_name = False
        if path:
            # exception, if not contain /, maybe it's just a filename
            if "/" not in path:
                name = "%s%s.avi" % (self.config.get_path_save_record(), path)
            else:
                # TODO need to add extension when giving all path with
                # filename?
                name = path
                if os.path.isdir(path):
                    add_format_name = True
        else:
            add_format_name = True
            # TODO mkdir if directory
            name = self.config.get_path_save_record()
        if add_format_name:
            name += "%s.avi" % time.strftime(
                "%Y_%m_%d_%H_%M_%S",
                time.gmtime())

        if os.path.isfile(name):
            log.print_function(logger.error, "File already exist %s" % name)
            return False

        self.file_name = name
        logger.info("Start record on path: %s", name)

        # 1 is best quality, 36 is worse
        qscale = compress * 0.35 + 1
        self.process = Popen(
            ['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r',
             '24',
             '-i', '-', '-vcodec', 'mpeg4', '-qscale', "%s" % qscale, '-r',
             '24', name], stdin=PIPE)
        self.media.add_observer(self.add_image)
        return True

    def add_image(self, image):
        # take sem with blocking
        self.sem.acquire(True)
        # check if process is active after the sem
        if self.process is None:
            self.sem.release()
            return
        # convert image to rgb in image2
        image2 = np.asarray(image, dtype="uint8")
        cv2.cvtColor(image, cv.CV_BGR2RGB, image2)
        # convert in PIL image
        img = Image.fromarray(image2, 'RGB')
        # Save it in ffmpeg process
        img.save(self.process.stdin, 'JPEG')
        self.sem.release()

    def get_file_name(self):
        if not self.file_name:
            return ""
        return self.file_name

    def stop(self):
        logger.info("Close record on path: %s", self.file_name)
        self.file_name = None
        if not self.process:
            return False
        self.media.remove_observer(self.add_image)
        self.sem.acquire(True)
        self.process.stdin.close()
        self.process.wait()
        self.process = None
        self.sem.release()
        return True
