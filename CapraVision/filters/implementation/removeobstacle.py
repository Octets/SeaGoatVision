
import cv2

from CapraVision.filters.filter import Filter

class RemoveObstacle(Filter):
    """Remove obstacles from an image"""
    
    def __init__(self):
        Filter.__init__(self)
        self.threshold = 230
        self.vertical_blur = 18
        self.horizontal_blur = 3
    
    def execute(self, image):
        blue, green, red = cv2.split(image)
        threshold = (red < self.threshold)
        red[threshold] = 0
        red = cv2.blur(red, (int(self.horizontal_blur), int(self.vertical_blur)))
        mask = red > 0
        image[mask] = 0
        
        return image
        
        