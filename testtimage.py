'''
Created on 2012-06-21

@author: benoit
'''

import cv2
from filters import hsvfilter, perspective

cv2.namedWindow('hohoho')
hsvf = hsvfilter.HSVFilter()
pers = perspective.Perspective()

run = True
hsv = False
perspec = False

while run:
    image = cv2
    if hsv:
        hsvf.execute(image)
    if perspec:
        image = pers.execute(image)
        
    cv2.imshow('hohoho', image)
    c = cv2.waitKey(1)
    
    if c == 104:
        hsv = not hsv
    elif c == 112:
        perspec = not perspec
    elif c == 113:
        run = False
    elif c != -1:
        print c
cv2.destroyAllWindows()
