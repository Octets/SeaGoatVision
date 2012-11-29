
import cv2
from CapraVision.server.filters.parameter import  Parameter

class RemoveObstacle:
    """Remove obstacles from an image"""
    
    def __init__(self):
        self.threshold = Parameter("Threshold",0,255,230)
        self.vertical_blur = Parameter("Vertical Blur",0,255,18)
        self.horizontal_blur = Parameter("Horizontal Blur",0,255,3)
    
    def execute(self, image):
        _, _, red = cv2.split(image)
        threshold = (red < self.threshold.get_current_value())
        red[threshold] = 0
        red = cv2.blur(red, (int(self.horizontal_blur.get_current_value()), int(self.vertical_blur.get_current_value())))
        mask = red > 0
        image[mask] = 0
        
        return image
        
        