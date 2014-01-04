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

import cv2
import os
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class Image_recorder:

    def __init__(self, media):
        self.writer = None
        self.media = media
        self.config = Configuration()
        self.file_name = None
        self.index = 0

    def start(self, shape, path=None, fps=30):
        # TODO manage multiple record
        # manage only one record at time
        if self.writer:
            self.stop()

        if not path:
            path = "%s" % (self.config.get_path_save_record())
            if not path:
                path = "./"
        elif "/" not in path:
            path = "%s%s" % (self.config.get_path_save_record(), path)

        if os.path.isfile(path):
            log.print_function(logger.error, "File already exist %s" % path)
            return False

        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except:
                pass

        self.file_name = path
        logger.info("Start record on path: %s", path)

        self.media.add_observer(self.write)
        self.writer = self.write
        return True

    def next_filename(self):
        path = os.path.join(self.file_name, str(self.index).zfill(10) + '.png')
        self.index += 1
        return path

    def write(self, image):
        cv2.imwrite(self.next_filename(), image)

    def get_file_name(self):
        if not self.file_name:
            return ""
        return self.file_name

    def stop(self):
        logger.info("Close record on path: %s", self.file_name)
        self.file_name = None
        if not self.writer:
            return False
        self.media.remove_observer(self.write)
        self.writer = None
        return True
