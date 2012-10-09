
import cv2

class RemoveObstacle:
    
    def __init__(self):
        pass
    
    def execute(self, image):
        image = cv2.blur(image, (3,3))
        blue, green, red = cv2.split(image.astype('uint16'))
        new_red = red**2
        threshold = (new_red < 62000)
        blue[threshold] = 0
        green[threshold] = 0
        red[threshold] = 0
        image[:,:,0] = blue
        image[:,:,1] = green 
        image[:,:,2] = red 
        return image