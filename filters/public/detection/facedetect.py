# http://docs.opencv.org/doc/tutorials/objdetect/cascade_classifier/cascade_classifier.html

import cv2
from cv2 import cv
import os
from SeaGoatVision.server.core.filter import Filter
from SeaGoatVision.commons.param import Param


class FaceDetection(Filter):
    """Detect faces and eyes"""

    def __init__(self):
        Filter.__init__(self)
        self.nb_face = 1
        # linux path
        path_frontal_face = os.path.join('/', 'usr', 'share', 'opencv',
                                         'haarcascades',
                                         'haarcascade_frontalface_alt.xml')
        self.face_detect_name = os.path.join(
            'data', 'facedetect', path_frontal_face)

        self.face_cascade = cv2.CascadeClassifier()
        self.face_cascade.load(self.face_detect_name)

        self.notify_filter = Param("notify", False)

    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cv2.equalizeHist(gray, gray)
        faces = self.face_cascade.detectMultiScale(gray,
                                                   1.1,
                                                   2,
                                                   0 | cv.CV_HAAR_SCALE_IMAGE,
                                                   (30, 30))
        for face in faces:
            self.draw_rectangle(image, face, (0, 0, 255))
        return image

    def draw_rectangle(self, image, coord, color):
        x, y, w, h = coord
        miny = y
        if miny < 0:
            miny = 0
        max_y = y + h
        if max_y > image.shape[0]:
            max_y = image.shape[0]
        minx = x
        if minx < 0:
            minx = 0
        max_x = x + w
        if max_x > image.shape[1]:
            max_x = image.shape[1]

        cv2.rectangle(image, (minx, miny), (max_x, max_y), color, 3)

        c_x = (max_x - minx) / 2 + minx
        c_y = (max_y - miny) / 2 + miny
        if self.notify_filter.get():
            self.notify_output_observers("facedetect%d : x=%d, y=%d" %
                                         (self.nb_face, c_x, c_y))
        self.nb_face += 1
        return image[miny:max_y, minx:max_x]
