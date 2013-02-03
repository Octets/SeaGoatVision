
# http://docs.opencv.org/doc/tutorials/objdetect/cascade_classifier/cascade_classifier.html

import cv2
import cv2.cv as cv

import os

class GetFirstFace:
    """Get first face detected in the image"""
    
    def __init__(self):
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
                                                   0|cv.CV_HAAR_SCALE_IMAGE, 
                                                   (30, 30)
                                                )
        for face in faces:
            return self.get_face(image, face)
            
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
    