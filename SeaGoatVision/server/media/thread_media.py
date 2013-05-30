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

class Thread_media(threading.Thread):
    """Media thread to process the images.
    """
    def __init__(self, media, sleep_time):
        threading.Thread.__init__(self)
        # self.daemon = True
        self.media = media
        self.running = False
        self.sleep_time = sleep_time
        self.pause = False

    def run(self):
        self.running = True
        for image in self.media:
            if image is None:
                time.sleep(self.sleep_time)
                continue

            # take a break if in pause
            while self.pause:
                time.sleep(self.sleep_time)

            start_time = time.time()
            self.media.notify_observer(image)
            if not self.running:
                break
            if self.sleep_time >= 0:
                sleep_time = self.sleep_time - (time.time() - start_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    time.sleep(0)
        self.running = False

    def stop(self):
        self.running = False
