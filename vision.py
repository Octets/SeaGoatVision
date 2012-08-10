'''
Created on 2012-07-26

@author: benoit
'''
import cv2
from filters import hsvfilter, perspective, toyuv, tohsv, rgbremove
from filters_window import FiltersWindow
import threading
import gobject

gobject.threads_init()

class Capture(threading.Thread):
    
    def __init__(self):
        pass
    
    def run(self):