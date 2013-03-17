
# http://docs.opencv.org/doc/tutorials/objdetect/cascade_classifier/cascade_classifier.html

import cv2
import cv2.cv as cv
import os
from SeaGoatVision.server.core.filter import Filter

class FaceDetection(Filter):
    """Detect faces and eyes"""

    def __init__(self):
        Filter.__init__(self)
        self.nb_face = 1
        self.eye_detect_name = os.path.join('data', 'facedetect',
                                        'haarcascade_eye_tree_eyeglasses.xml')
        self.face_detect_name = os.path.join('data', 'facedetect',
                                             'haarcascade_frontalface_alt.xml')
        self.eye_cascade = cv2.CascadeClassifier()
        self.face_cascade = cv2.CascadeClassifier()
        assert self.eye_cascade.load(self.eye_detect_name)
        assert self.face_cascade.load(self.face_detect_name)

    def execute(self, image):
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        cv2.equalizeHist(gray, gray)
        faces = self.face_cascade.detectMultiScale(gray,
                                                   1.1,
                                                   2,
                                                   0|cv.CV_HAAR_SCALE_IMAGE,
                                                   (30, 30)
                                                )
        for face in faces:
            faceimg = self.draw_rectangle(image, face, (0, 0, 255))

            """eyes = self.eye_cascade.detectMultiScale(faceimg,
                                                   1.1,
                                                   2,
                                                   0|cv.CV_HAAR_SCALE_IMAGE,
                                                   (30, 30)
                                                )
            for eye in eyes:
                self.draw_rectangle(image,
                        (face[0] + eye[0], face[1] + eye[1], eye[2], eye[3]),
                        (255, 0, 0))"""

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

        cv2.rectangle(image, (minx, miny), (maxx, maxy), color, 3)

        c_x = (maxx-minx) / 2 + minx
        c_y = (maxy-miny) / 2 + miny
        self.notify_output_observers("facedetect%d : x=%d, y=%d" % \
                (self.nb_face, c_x, c_y))
        self.nb_face += 1
        return image[miny:maxy, minx:maxx]

