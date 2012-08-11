'''
Created on 2012-06-21

@author: benoit
'''

import cv2
from filters import *
from filters_utils import *
from gui_filters import *
import gui

import threading
import gobject
import gtk

gtk.disable_setlocale()
gtk.init_check()
gobject.threads_init()
gtk.gdk.threads_init()

video = cv2.VideoCapture(0)

#pers = Perspective()
#rgbrem = RGBLevel()
#rgbthres = RGBThreshold()

#win = map_filter_to_ui(pers)
#w = win(pers)
#w.window.show_all()

#winRGBLevel = WinRGBLevel(rgbrem)
#winRGBLevel.window.show_all()

#winRGBThreshold = WinRGBThreshold(rgbthres)
#winRGBThreshold.window.show_all()

#winPerspective = WinPerspective(pers)
#winPerspective.window.show_all()

#winFilters = WinFilterChain()
#winFilters.window.show_all()

def source_video():
    run, image = video.read()
    return image

def source_image():
    image = cv2.imread('0-157.png')
    return image

class Capture(threading.Thread):
    def __init(self):
        pass
    
    def run(self):
        run = True

        while run:
            #image = source_image()
            image = source_video()
            cv2.imshow('init', image)

            #image = pers.execute(image)
            #cv2.imshow('perspec', image)
            
            #image = rgbrem.execute(image)
            #cv2.imshow('rgbrem', image)
            
            #image = rgbthres.execute(image)
            #cv2.imshow('rgbthres', image)
        
            c = cv2.waitKey(1)
    
#c = Capture()
#print "Start capture"
#c.start()
#print "ok"
#t = threading.Thread(target=gtk.main, name="GTK Thread")
#t.deamon = True
#t.start()

run = True
while run:
    print "running"
    #image = source_image()
    image = source_video()
    cv2.imshow('init', image)
    print "avant wait"
    try:
        c = cv2.waitKey(1)
    except e:
        print e
    print "apres wait"

#gtk.main()
print "apres gtk main"
cv2.destroyAllWindows()
print "almost done"
c.stop()
print "done"