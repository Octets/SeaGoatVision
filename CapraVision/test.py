import unittest

import pygtk
import gtk
import cv2
import gui, source, chain
from filters import noop
import gobject
gobject.threads_init()

def source_image():
    image = cv2.imread('0-157.png')
    return image

def test_viewer():
    s = source.Webcam(0)
    c = chain.FilterChain()
    c.add_filter(noop)
    w = gui.WinViewer(s, c, noop)
    w.window.show_all()
    gtk.main()
    
if __name__ == '__main__':
    print "test"
    test_viewer()