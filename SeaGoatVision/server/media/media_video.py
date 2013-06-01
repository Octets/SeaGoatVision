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
from SeaGoatVision.commons.keys import *

class Media_video(Media):
    def __init__(self):
        Media.__init__(self)
        self.file_name = None
        self.lst_file = []
        self.pos = 0
        self.video = None
        self.last_image = None
        self.is_playing = False
        self.active_loop = True

    def is_media_streaming(self):
        return False

    def is_media_video(self):
        return True

    def get_type_media(self):
        return get_media_type_video_name()

    def open(self):
        Media.open(self)
        self.play()

    def _open_video(self):
        video = cv2.VideoCapture(self.file_name)
        if video:
            self.video = video
            return True
        return False

    def do_cmd(self, action):
        if not self.thread:
            return False
        if action == get_key_media_play():
            if self.thread.pause:
                self.thread.pause = False
                return True
        elif action == get_key_media_pause():
            if not self.thread.pause:
                self.thread.pause = True
                return True
        elif action == get_key_media_loop():
            self.set_loop_enable(not self.active_loop)
        return False

    def set_file(self, file_name):
        self.file_name = file_name
        # a file can be a directory
        if os.path.isdir(file_name):
            self.lst_image = self.find_all_images(file_name)
            return True
        # check if it's an image
        image = cv2.imread(file_name)
        if image is not None:
            self.pos = 0
            self.lst_image = [file_name]
            return True
        # check if it's supported video
        return self._open_video()

    def set_loop_enable(self, enable):
        self.active_loop = enable

    def play(self):
        self.is_playing = True

    def pause(self):
        self.is_playing = False

    def next(self):
        if self.video:
            if not self.is_playing:
                if self.last_image:
                    return self.last_image.copy()
                else:
                    return None
            run, image = self.video.read()
            if not run:
                if not self.active_loop or not self._open_video():
                    return None
                run, image = self.video.read()
                if not run:
                    raise StopIteration
            self.last_image = image
            return self.last_image.copy()

        if not self.lst_image:
            return None
        if self.pos >= len(self.lst_image):
            self.pos = 0
        image = cv2.imread(self.lst_image[self.pos])
        self.pos += 1
        return image.copy()

    def find_all_images(self, folder):
        """Receive a directory as parameter.
            Find all files that are images in all sub-directory.
            Returns a list of those files"""
        images = []
        for root, _, files in os.walk(folder):
            for filename in files:
                path = os.path.join(root, filename)
                image = cv2.imread(path)
                if image is not None:
                    images.append(path)
        list.sort(images)
        return images
