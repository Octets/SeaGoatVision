
import cv2
import cv2.cv as cv
import numpy as np

from CapraVision.server.filters.parameter import  Parameter

class HistoThresh:
    
    def __init__(self):
        self.channel1 = Parameter("Channel 1", 0, 1, 1)
        self.channel1_min = Parameter("Channel 1 min", 1, 255, 1)
        self.channel1_max = Parameter("Channel 1 max", 1, 255, 255)
        self.channel1_size = Parameter("Channel 1 size", 0, 255, 100)
        
        self.channel2 = Parameter("Channel 2", 0, 1, 1)
        self.channel2_min = Parameter("Channel 2 min", 1, 255, 1)
        self.channel2_max = Parameter("Channel 2 max", 1, 255, 255)
        self.channel2_size = Parameter("Channel 2 size", 0, 255, 100)
        
        self.channel3 = Parameter("Channel 3", 0, 1, 1)
        self.channel3_min = Parameter("Channel 3 min", 1, 255, 1)
        self.channel3_max = Parameter("Channel 3 max", 1, 255, 255)
        self.channel3_size = Parameter("Channel 3 size", 0, 255, 100)
            
        self.threshold = Parameter("Threshold", 0, 255, 80)
        self.max_value = Parameter("Max Value", 0, 255, 255)
                            
    def configure(self):
        pass
    
    def execute(self, image):
        channels = []
        chranges = []
        sizes = []
        
        if self.channel1.get_current_value() == 1:
            channels.append(0)
            chranges.append(self.channel1_min.get_current_value())
            chranges.append(self.channel1_max.get_current_value())
            sizes.append(self.channel1_size.get_current_value())
            
        if self.channel2.get_current_value() == 1:
            channels.append(1)
            chranges.append(self.channel2_min.get_current_value())
            chranges.append(self.channel2_max.get_current_value())
            sizes.append(self.channel2_size.get_current_value())
            
        if self.channel3.get_current_value() == 1:
            channels.append(2)
            chranges.append(self.channel3_min.get_current_value())
            chranges.append(self.channel3_max.get_current_value())
            sizes.append(self.channel3_size.get_current_value())
            
        hist = cv2.calcHist([image], 
                            channels, 
                            None, 
                            sizes, 
                            chranges)
            
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                
        image = cv2.calcBackProject([image], channels, hist, chranges, 1)

        _, image = cv2.threshold(image, 
                                 self.threshold.get_current_value(), 
                                 self.max_value.get_current_value(), 0)
        
        return cv2.merge((image, image, image))
    
