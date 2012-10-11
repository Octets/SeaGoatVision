
import cv2

class RemoveObstacle:
    
    def __init__(self):
        self.threshold = 50000
        self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3), (0,0))
    
    def execute(self, image):
        blue, green, red = cv2.split(image.astype('uint16'))
        new_red = red**2
        threshold = (new_red < self.threshold)
        red[threshold] = 0
        red = cv2.morphologyEx(
                  red, cv2.MORPH_CLOSE, self._kernel, iterations=10)
        mask = red > 0
        image[mask] = 0
        
        #blue[threshold] = 0
        #green[threshold] = 0
        #red[threshold] = 0
        #image[:,:,0] = blue
        #image[:,:,1] = green 
        #image[:,:,2] = red 
        return image
        
        