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
import time
import threading
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class Thread_media(threading.Thread):
    """Media thread to process the images.
    """
    def __init__(self, media):
        threading.Thread.__init__(self)
        # self.daemon = True
        self.media = media
        self.running = False
        self.pause = False

    def run(self):
        sleep_time_per_fps = self.media.sleep_time
        self.running = True
        protection_max_reset = 3
        no_reset = 0
        while self.running:
            try:
                image = self.media.next()
                no_reset = 0
            except StopIteration:
                if self.media.active_loop:
                    self.media.reset()
                    no_reset += 1
                    if no_reset >= protection_max_reset:
                        self.running = False
                        log.print_function(logger.error, "Max reset - close media %s" % self.media.get_name())
                    continue
                else:
                    while not self.media.active_loop:
                        if not self.running:
                            return
                        time.sleep(sleep_time_per_fps)

            if image is None:
                time.sleep(sleep_time_per_fps)
                continue

            # take a break if in pause
            while self.pause:
                if not self.running:
                    return
                time.sleep(sleep_time_per_fps)

            start_time = time.time()
            self.media.notify_observer(image)
            if not self.running:
                break
            if sleep_time_per_fps > 0:
                sleep_time = sleep_time_per_fps - (time.time() - start_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        self.running = False

    def stop(self):
        self.running = False
