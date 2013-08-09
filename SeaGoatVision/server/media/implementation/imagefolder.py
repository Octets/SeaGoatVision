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

import cv2
import os

class ImageFolder:
    def __init__(self):
        self.file_names = []
        self.pos = 0

    def set_pos(self, value):
        self.pos = value

    def read_image(self, image_path):
        self.file_names = [image_path]
        self.pos = 0

    def read_folder(self, folder):
        self.file_names = self._find_all_images(folder)
        self.pos = 0

    def next(self):
        if not self.file_names:
            return None
        if self.pos > len(self.file_names):
            self.pos = 0
            raise StopIteration

        image = self._load_image(self.pos)
        self.pos += 1
        return image

    def _load_image(self, pos):
        image = self.current_file_name(pos)
        return cv2.imread(image)

    def current_pos(self):
        return self.pos

    def current_file_name(self, pos= -1):
        if pos == -1:
            pos = self.pos
        return self.file_names[pos]

    def get_total_frames(self):
        return len(self.file_names)

    def reset_pos(self):
        self.pos = 0

    def _find_all_images(self, folder):
        """Receive a directory as parameter.
            Find all files that are images in all sub-directory.
            Returns a list of those files"""
        images = []
        for root, _, files in os.walk(folder):
            for filename in files:
                path = os.path.join(root, filename)
                # TODO do we need to check if file is real image??
                #image = cv2.imread(path)
                #if image is not None:
                #    images.append(path)
                images.append(path)
        list.sort(images)
        return images
