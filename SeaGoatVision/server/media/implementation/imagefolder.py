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

class ImageFolder(Media_video):

    def __init__(self):
        Media_video.__init__(self)
        self.folder_name = ''
        self.file_names = []
        self.position = 0
        self.return_file_name = False
        self.auto_increment = True

    def set_auto_increment(self, value):
        self.auto_increment = value

    def set_return_file_name(self, value):
        self.return_file_name = value

    def set_position(self, value):
        self.position = value

    def read_folder(self, folder):
        self.file_names = self.find_all_images(folder)
        self.folder_name = folder
        self.position = 0

    def next(self):
        if len(self.file_names) == 0:
            return None
        elif self.position >= len(self.file_names):
            self.position = 0
            raise StopIteration
        else:
            image = self.load_image(self.position)
            file_name = self.file_names[self.position]
            if self.auto_increment:
                self.position += 1
            if self.return_file_name:
                return (file_name, image)
            else:
                return image

    def load_image(self, position):
        image = self.current_file_name(position)
        return cv2.imread(image)

    def current_position(self):
        return self.position

    def current_file_name(self, position= -1):
        if position == -1:
            position = self.position

        return self.file_names[position]

    def total_images(self):
        return len(self.file_names)

    def reset_position(self):
        self.position = 0
