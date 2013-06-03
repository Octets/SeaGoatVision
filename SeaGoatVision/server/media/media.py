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

from thread_media import Thread_media
import numpy as np

class Media:
    def __init__(self):
        self.sleep_time = 1 / 30.0
        self.lst_observer = []
        self.thread = None
        self.media_name = None

    def is_media_streaming(self):
        # complete it into media_streaming and media_video
        pass

    def is_media_video(self):
        # complete it into media_streaming and media_video
        pass

    def get_type_media(self):
        # complete it into media_streaming and media_video
        # type is Video or Streaming
        pass

    def get_name(self):
        return self.media_name

    def __iter__(self):
        return self

    def open(self):
        # IMPORTANT, if inherit, call this at the end
        # the thread need to be start when device is ready
        if self.thread:
            return
        self.thread = Thread_media(self, self.sleep_time)
        self.thread.start()

    def next(self):
        # edit me in child
        pass

    def close(self):
        if not self.thread:
            return
        self.thread.stop()
        self.thread = None

    def change_sleep_time(self, sleep_time):
        self.sleep_time = sleep_time
        if self.thread is not None:
            self.thread.sleep_time = sleep_time

    def add_observer(self, observer):
        start_media = False
        if not self.lst_observer:
            start_media = True
        self.lst_observer.append(observer)
        if start_media:
            self.open()

    def remove_observer(self, observer):
        self.lst_observer.remove(observer)
        if not self.lst_observer:
            self.close()

    def notify_observer(self, image):
        # be sure the image is different for all observer
        for observer in self.lst_observer:
            observer(np.copy(image))
