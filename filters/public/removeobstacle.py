
import cv2
import cv2.cv as cv

from SeaGoatVision.commun.param import  Param
from SeaGoatVision.server.core.filter import Filter

class RemoveObstacle(Filter):
    """Remove obstacles from an image"""

    def __init__(self):
        Filter.__init__(self)
        self.threshold = Param("Threshold", 12, min_v=0, max_v=255)
        #self.vertical_blur = Param("Vertical Blur", 18, min_v=0, max_v=255)
        #self.horizontal_blur = Param("Horizontal Blur", 3, min_v=0, max_v=255)

    def execute(self, image):
        # copy = cv2.cvtColor(image, cv.CV_BGR2HSV)
        copy = cv2.blur(image, (3, 3))
        h, _, _ = cv2.split(copy)
        h[h > self.threshold.get()] = 0
        contours, _ = cv2.findContours(
                                   h,
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
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


