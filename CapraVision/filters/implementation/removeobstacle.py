
import cv2

class RemoveObstacle:
    """Remove obstacles from an image"""
    
    def __init__(self):
        self.threshold = 230
        self.vertical_blur = 18
        self.horizontal_blur = 3
    
    def execute(self, image):
        blue, green, red = cv2.split(image)
        threshold = (red < self.threshold)
        red[threshold] = 0
        red = cv2.blur(red, (self.horizontal_blur, self.vertical_blur))
        mask = red > 0
        image[mask] = 0
        
        return image
        
        