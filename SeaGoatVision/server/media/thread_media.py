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
import time
import threading
from SeaGoatVision.commons import log
import media
import numpy as np

logger = log.get_logger(__name__)


class ThreadMedia(threading.Thread):
    """Media thread to process the images.
    """

    def __init__(self, media, publisher, rotate_param):
        threading.Thread.__init__(self)
        # self.daemon = True
        self.media = media
        self.running = False
        self.pause = False
        self.nb_fps = 0
        self.publisher = publisher
        self.rotate_param = rotate_param

    def run(self):
        sleep_time_per_fps = self.media.sleep_time
        self.running = True
        protection_max_reset = 3
        no_reset = 0
        nb_busy = 0
        first_fps_time = time.time()
        nb_fps = 0
        image = None
        msg_error = "Max reset - close media %s" % self.media.get_name()
        self.media.set_status(media.MediaStatus.run)
        rotate_param = self.rotate_param

        while self.running:
            # TODO try to remove this try catch for better performance
            try:
                image = self.media.next()
                no_reset = 0
                # apply rotate picture
                angle = rotate_param.get()
                if angle:
                    image = np.rot90(image, angle)
            except StopIteration:
                if self.media.active_loop:
                    self.media.reset()
                    no_reset += 1
                    if no_reset >= protection_max_reset:
                        self.running = False
                        log.print_function(logger.error, msg_error)
                    continue
                else:
                    while not self.media.active_loop:
                        if not self.running:
                            return
                        time.sleep(sleep_time_per_fps)

            if image is None:
                # if receive no image since 1 sec, the camera is maybe busy
                nb_busy += 1
                if nb_busy > self.media.fps:
                    self.media.set_status(media.MediaStatus.busy)
                time.sleep(sleep_time_per_fps)
                continue
            nb_busy = 0
            nb_fps += 1

            # take a break if in pause
            while self.pause:
                self.media.set_status(media.MediaStatus.pause)
                if not self.running:
                    return
                time.sleep(sleep_time_per_fps)
            self.media.set_status(media.MediaStatus.run)

            if not self.running:
                return

            start_time = time.time()
            if start_time - first_fps_time > 1:
                self.publisher({"fps": nb_fps})
                self.nb_fps = nb_fps
                nb_fps = 0
                first_fps_time = start_time
            self.media.notify_observer(image)
            if not self.running:
                break
            if sleep_time_per_fps > 0:
                sleep_time = sleep_time_per_fps - (time.time() - start_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        self.running = False

    def get_fps(self):
        return self.nb_fps

    def stop(self):
        self.running = False
        self.media.set_status(media.MediaStatus.close)
