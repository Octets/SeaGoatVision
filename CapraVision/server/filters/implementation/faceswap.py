
# http://docs.opencv.org/doc/tutorials/objdetect/cascade_classifier/cascade_classifier.html

import cv2
import cv2.cv as cv
import numpy as np

import os
import sys

class FaceSwap:
    """Swap faces"""
    
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
        for i in xrange(0, len(faces)):
            lastface = faces[i-1]
            face = faces[i]
            lastrect = self.get_image_size(image, face)
            face = cv2.resize(face, (lastmaxy-lastminy, lastmaxx-lastminx))
            
            
            
            faceimg, coord = self.get_image_data(image, face)
            y, x, _ = faceimg.shape
            if x < smallestx:
                smallestx = x
            if y < smallesty:
                smallesty = y
            facedata.append((faceimg, coord))
            
        for i in xrange(0, len(facedata)):
            _, lastcoord = facedata[i-1]
            lastminy, lastmaxy, lastminx, lastmaxx = lastcoord

            face, coord = facedata[i]
            miny, maxy, minx, maxx = coord
            
            face = cv2.resize(face, (lastmaxy-lastminy, lastmaxx-lastminx))             
            welp = image[lastminy:lastmaxy, 
                  lastminx:lastmaxx]
            
            image[lastminy:lastmaxy, 
                  lastminx:lastmaxx] = cv2.addWeighted(welp, 0.5, face, 0.5, 0.0)#cv2.merge((gray,gray,gray))
                  
        return image

    def get_image_size(self, image, coord):
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
    
        return (miny, maxy, minx, maxx)
    
    def convexhull(self, gray):
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cnt, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnt:
            hull = cv2.convexHull(c)
            cv2.drawContours(mask, [hull],-1, 255, -1)    
        return mask
