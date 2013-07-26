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

import os
import cv2
from media import Media
from implementation.movie import Movie
from implementation.imagefolder import ImageFolder
from SeaGoatVision.commons.keys import *

class Media_video(Media):
    def __init__(self, name):
        super(Media_video, self).__init__()
        self.movie = None
        self.imagefolder = None

        self.media_name = name
        self.file_name = None
        self.is_playing = False

    def is_media_streaming(self):
        return False

    def is_media_video(self):
        return True

    def reset(self):
        if self.movie:
            self.movie.reset()

    def get_type_media(self):
        return get_media_type_video_name()

    def open(self):
        Media.open(self)
        self.play()

    def get_total_frames(self):
        if self.movie:
            return self.movie.get_total_frames()
        elif self.imagefolder:
            return self.imagefolder.get_total_frames()
        return -1

    def do_cmd(self, action, value):
        if not self.thread and not self.is_client_manager:
            return False
        if action == get_key_media_play():
            if self.thread.pause:
                self.thread.pause = False
                return True
            return False
        elif action == get_key_media_pause():
            if not self.thread.pause:
                self.thread.pause = True
                return True
            return False
        elif action == get_key_media_loop():
            self.set_loop_enable(not self.active_loop)
        elif action == set_key_media_frame():
            self.change_frame(value)
        else:
            return False
        return True

    def change_frame(self, value):
        if self.movie:
            self.movie.set_position(value)
            self.notify_observer(self.movie.next())
        elif self.imagefolder:
            self.imagefolder.set_pos(value)
            self.notify_observer(self.imagefolder.next())

    def set_file(self, file_name):
        self.file_name = file_name
        # a file can be a directory
        if os.path.isdir(file_name):
            self.imagefolder = ImageFolder()
            self.imagefolder.read_folder(file_name)
            return True
        # check if it's an image
        image = cv2.imread(file_name)
        if image is not None:
            self.imagefolder = ImageFolder()
            self.imagefolder.read_image(file_name)
            return True
        #if the file is not a video, videocapture not return None
        # check if it's supported video
        video = cv2.VideoCapture(file_name)
        if video:
            self.movie = Movie(file_name)
            return True
        return False

    def play(self):
        self.is_playing = True

    def pause(self):
        self.is_playing = False

    def next(self):
        if self.movie:
            return self.movie.next()
        if self.imagefolder:
            return self.imagefolder.next()
        return None
