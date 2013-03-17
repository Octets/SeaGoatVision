
import cv2
import numpy as np
from SeaGoatVision.server.core.filter import Filter

class BGR2HSVManual(Filter):
    def __init__(self):
        Filter.__init__(self)

    def execute(self, image):
        b, g, r = cv2.split(image)
        b = b.astype(np.float16) / 255.0
        g = g.astype(np.float16) / 255.0
        r = r.astype(np.float16) / 255.0
        
        max_rgb = np.maximum(np.maximum(b, g), r)
        min_rgb = np.minimum(np.minimum(r, g), b)
        
        v = max_rgb
        
        s = np.zeros(v.shape, v.dtype)
        s[v != 0] = ((v - min_rgb) / v)[v != 0]
        s[v == 0] = 0
        
        h = np.zeros(v.shape, v.dtype)
        h[v == r] = (60 * (g - b) / v)[v == r]
        h[v == g] = (120 + 60 * (b - r) / (v - min_rgb))[v == g]
        h[v == b] = (240 + 60 * (r - g) / (v - min_rgb))[v == b]
        
        h[h < 0] += 360
        h = h / 2
        s = s * 255
        v = v * 255
        
        image = cv2.merge((h.astype(np.uint8),
                           s.astype(np.uint8),
                           v.astype(np.uint8)))
        
        return image 
    
