#!/usr/bin/env python

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

import os
import cv2
from cv2 import cv
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter


class ExePy2(Filter):
    """
    Python Example Test #2
    Example filter to test params.
    Show rectangle on each detected face.
    """

    def __init__(self):
        Filter.__init__(self)
        self.dct_color_choose = {"red": (0, 0, 255), "green": (0, 255, 0), "blue": (255, 0, 0)}
        self.color_rect = self.dct_color_choose["red"]
        self.i_text_size = 1.0
        # add params
        self.show_output = Param("enable_output", True)
        self.show_output.set_description("Enable to show rectangle.")

        self.color_rectangle = Param("color_rectangle", "red",
                                     lst_value=self.dct_color_choose.keys())
        self.color_rectangle.set_description("Change the RGB color of the rectangle.")
        self.color_rectangle.add_group("rectangle")

        self.show_rectangle = Param("show_rectangle", True)
        self.show_rectangle.set_description("Colorize a rectangle around the face.")
        self.show_rectangle.add_group("rectangle")

        self.border_rec_size = Param("border_rec_size", 3, min_v=1, max_v=9)
        self.border_rec_size.set_description("Change the border size of the rectangle.")
        self.border_rec_size.add_group("rectangle")

        self.show_text = Param("enable_text", True)
        self.show_text.set_description("Show text upper the rectangle.")
        self.show_text.add_group("message")

        self.text_face = Param("text_face", "")
        self.text_face.set_description("The text to write on the rectangle.")
        self.text_face.add_group("message")

        self.text_size = Param("text_size", self.i_text_size, min_v=0.1, max_v=4.9)
        self.text_size.set_description("Change the text size.")
        self.text_size.add_group("message")

        self.nb_face = 1
        self.eye_detect_name = os.path.join('data', 'facedetect',
                                            'haarcascade_eye_tree_eyeglasses.xml')
        self.face_detect_name = os.path.join('data', 'facedetect',
                                             'haarcascade_frontalface_alt.xml')
        self.eye_cascade = cv2.CascadeClassifier()
        self.face_cascade = cv2.CascadeClassifier()
        self.eye_cascade.load(self.eye_detect_name)
        self.face_cascade.load(self.face_detect_name)

    def configure(self):
        self.color_rect = self.dct_color_choose[self.color_rectangle.get()]
        self.i_text_size = self.text_size.get()

    def execute(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(gray, gray)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 2, 0 | cv.CV_HAAR_SCALE_IMAGE,
                                                   (30, 30))
        for face in faces:
            self.draw_rectangle(image, face, self.color_rect, self.i_text_size)
            self.nb_face = 1

        return image

    def draw_rectangle(self, image, coord, color, txt_size):
        x, y, w, h = coord
        min_y = y
        if min_y < 0:
            min_y = 0
        min_face_y = min_y - 10
        if min_face_y < 0:
            min_face_y = 0
        max_y = y + h
        if max_y > image.shape[0]:
            max_y = image.shape[0]
        min_x = x
        if min_x < 0:
            min_x = 0
        max_x = x + w
        if max_x > image.shape[1]:
            max_x = image.shape[1]

        if self.show_rectangle.get():
            cv2.rectangle(image, (min_x, min_y), (max_x, max_y), color,
                          thickness=self.border_rec_size.get())
        if self.show_text.get():
            text = "%s.%s" % (self.nb_face, self.text_face.get())
            cv2.putText(image, text, (min_x, min_face_y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, txt_size,
                        color)

        # note: >> 2 == / 2
        c_x = (max_x - min_x) >> 2 + min_x
        c_y = (max_y - min_y) >> 2 + min_y
        if self.show_output.get():
            self.notify_output_observers(
                "face detect no %d : x=%d, y=%d" % (self.nb_face, c_x, c_y))
        self.nb_face += 1
