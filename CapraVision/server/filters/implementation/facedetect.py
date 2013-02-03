
import cv2
import cv2.cv as cv

import os

class FaceDetection:
    
    def __init__(self):
        self.eye_detect_name = os.path.join('data', 
                                        'facedetect', 
                                        'haarcascade_eye_tree_eyeglasses.xml')
        self.face_detect_name = os.path.join('data', 
                                             'facedetect', 
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
        for x, y, width, height in faces:
            cv2.rectangle(image, (x, y), (x+width, y+height), 
                          (0, 0, 255))
    
        return image
    