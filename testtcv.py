'''
Created on 2012-06-16

@author: benoit
'''

import cv2.cv as cv

#import hsvfilter

def filtreHSV():
    pass

def faireRectangle(image):
    cv.Rectangle(image, (0,0), (100, 100), (0,0,0), cv.CV_FILLED)

cv.NamedWindow('hohoho')
capture = cv.CaptureFromCAM(-1)
run = True
hsv = False
rect = False

while run:
    image = cv.QueryFrame(capture)
    if rect:
        faireRectangle(image)
    if hsv:
        pass
        #image = hsvfilter.execute(image)
    cv.ShowImage('hohoho', image)
    c = cv.WaitKey(10)
    if c == 104: # H
        hsv = not hsv
    elif c == 105: # I
        print 'height: ' + str(image.height) + ' width: ' + str(image.width)
    elif c == 113: # Q
        run = False
    elif c == 114: # R
        print 'rectangle!'
        rect = not rect
    elif c == 115: # S
        print 'Saving image'
        cv.SaveImage('capture.png', image)
    elif c != -1:
        print c

#if __name__ == '__main__':
#    pass