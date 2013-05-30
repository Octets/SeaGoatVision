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

from media import Media
from SeaGoatVision.commons.keys import *

class Media_video(Media):
    def __init__(self):
        Media.__init__(self)
        self.file_name = None

    def is_media_streaming(self):
        return False

    def is_media_video(self):
        return True

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
        return False

    def get_type_media(self):
        return get_media_type_video_name()

    def set_file(self, file_name):
        # a file can be a directory
        self.file_name = file_name

    def find_all_images(self, folder):
        """Receive a directory as parameter.
            Find all files that are images in all sub-directory.
            Returns a list of those files"""
        images = []
        for root, _, files in os.walk(folder):
            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext in supported_image_formats():
                    images.append(os.path.join(root, filename))
        list.sort(images)
        return images
