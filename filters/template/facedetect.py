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
import cv2.cv as cv
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter

# Heritence of Filter is facultatif if you need framework tools.
# you have access to :
# self.get_params(param_name=None) to get a list or object of Params
# self.notify_output_observers(string) to send a notification to observer

# Reserved function
# self.add_output_observer(observer) to add a function observer
# self.remove_output_observer(observer) to remove a function observer


class FaceDetection(Filter):

    """Detect faces and eyes"""

    def __init__(self):
        Filter.__init__(self)
        self.nb_face = 1
        self.eye_detect_name = os.path.join(
            'data',
            'facedetect',
            'haarcascade_eye_tree_eyeglasses.xml')
        self.face_detect_name = os.path.join(
            'data',
            'facedetect',
            'haarcascade_frontalface_alt.xml')
        self.eye_cascade = cv2.CascadeClassifier()
        self.face_cascade = cv2.CascadeClassifier()
        self.eye_cascade.load(self.eye_detect_name)
        self.face_cascade.load(self.face_detect_name)
        self.show_rectangle = Param("show_rectangle", True)

        # To share parameter between filter, create it with :
        self.add_global_params(Param("width", 3, min_v=1, max_v=10))
        # On the execution, use it like this :
        param = self.get_global_params("width")

    def configure(self):
        # This is called when param is modify
        pass

    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cv2.equalizeHist(gray, gray)
        faces = self.face_cascade.detectMultiScale(gray,
                                                   1.1,
                                                   2,
                                                   0 | cv.CV_HAAR_SCALE_IMAGE,
                                                   (30, 30)
                                                   )
        for face in faces:
            faceimg = self.draw_rectangle(image, face, (0, 0, 255))
            self.nb_face = 1

        return image

    def draw_rectangle(self, image, coord, color):
        x, y, w, h = coord
        miny = y
        if miny < 0:
            miny = 0
        maxy = y + h
        if maxy > image.shape[0]:
            maxy = image.shape[0]
        minx = x
        if minx < 0:
            minx = 0
        maxx = x + w
        if maxx > image.shape[1]:
            maxx = image.shape[1]

        if self.show_rectangle.get():
            cv2.rectangle(image, (minx, miny), (maxx, maxy), color, 3)

        c_x = (maxx - minx) / 2 + minx
        c_y = (maxy - miny) / 2 + miny
        self.notify_output_observers(
            "facedetect%d : x=%d, y=%d" %
            (self.nb_face, c_x, c_y))
        self.nb_face += 1
        return image[miny:maxy, minx:maxx]
