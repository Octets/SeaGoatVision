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

from SeaGoatVision.server.media.media_video import Media_video
import cv2
import cv2.cv as cv

class Movie(Media_video):

    def __init__(self):
        Media_video.__init__(self)
        self.video = None
        self.isplaying = True
        self.last_image = None

    def open(self):
        Media_video.open(self)
        self.open_file()
        self.play()

    def open_file(self):
        self.video = cv2.VideoCapture(self.file_name)

    def play(self):
        self.isplaying = True

    def pause(self):
        self.isplaying = False

    def is_opened(self):
        return self.video.isOpened()

    def get_width(self):
        return self.video.get(cv.CV_CAP_PROP_FRAME_WIDTH)

    def set_width(self, width):
        self.video.set(cv.CV_CAP_PROP_FRAME_WIDTH, width)

    def get_height(self):
        return self.video.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

    def set_height(self, height):
        self.video.set(cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    def get_fps(self):
        return self.video.get(cv.CV_CAP_PROP_FPS)

    def set_fps(self, fps):
        self.video.set(cv.CV_CAP_PROP_FPS, fps)

    def get_position(self):
        return self.video.get(cv.CV_CAP_PROP_POS_FRAMES)

    def set_position(self, pos):
        self.video.set(cv.CV_CAP_PROP_POS_FRAMES, pos)

    def get_total_frames(self):
        return self.video.get(cv.CV_CAP_PROP_FRAME_COUNT)

    def next(self):
        if self.video is None or not self.video.isOpened():
            return None
        elif not self.isplaying:
            return self.last_image.copy()

        run, self.last_image = self.video.read()
        if not run:
            # TODO hack to loop
            self.open_file()
            run, self.last_image = self.video.read()
            if not run:
                raise StopIteration

        return self.last_image.copy()

    def close(self):
        Media_video.close(self)
        if self.video is not None:
            self.video.release()
