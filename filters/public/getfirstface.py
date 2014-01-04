
# http://docs.opencv.org/doc/tutorials/objdetect/cascade_classifier/cascade_classifier.html

import cv2
from cv2 import cv
import numpy as np

import os
from SeaGoatVision.server.core.filter import Filter


class GetFirstFace(Filter):

    """Get first face detected in the image"""

    def __init__(self):
        Filter.__init__(self)
        self.face_detect_name = os.path.join('data',
                                             'facedetect',
                                             'haarcascade_frontalface_alt.xml')
        self.face_cascade = cv2.CascadeClassifier()
        assert self.face_cascade.load(self.face_detect_name)

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
            faceimg = self.get_face(image, face)
            mask = np.zeros(
                (image.shape[0],
                 image.shape[1],
                 1),
                dtype=np.uint8)
            rect = (face[0], face[1], face[0] + face[2], face[1] + face[3])
            bgd_model = np.zeros((1, 5 * 13))
            fgd_model = np.zeros((1, 5 * 13))
            cv2.grabCut(
                image,
                mask,
                rect,
                bgd_model,
                fgd_model,
                10,
                mode=cv2.GC_INIT_WITH_RECT)
            b, g, r = cv2.split(image)
            b[mask == cv2.GC_BGD] = 255
            g[mask == cv2.GC_BGD] = 255
            r[mask == cv2.GC_BGD] = 255

    def get_face(self, image, coord):
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

        return image[miny:maxy, minx:maxx]
