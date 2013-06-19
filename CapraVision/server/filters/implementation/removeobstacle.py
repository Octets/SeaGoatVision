
import cv2
import cv2.cv as cv

from CapraVision.server.filters.parameter import  Parameter

class RemoveObstacle:
    """Remove obstacles from an image"""
    
    def __init__(self):
        self.threshold = Parameter("Threshold",0,255,12)
        self.vertical_blur = Parameter("Vertical Blur",0,255,18)
        self.horizontal_blur = Parameter("Horizontal Blur",0,255,3)
    
    def execute(self, image):
        copy = cv2.cvtColor(image, cv.CV_BGR2HSV)
        copy = cv2.blur(copy, (3,3))
        h, _, _ = cv2.split(copy)
        h[h > self.threshold.get_current_value()] = 0
        contours, _ = cv2.findContours(
                                   h, 
                                   cv2.RETR_TREE, 
                                   cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            miny = y - h
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
            image[miny:maxy, minx:maxx] = 0
        
        return image
        
        