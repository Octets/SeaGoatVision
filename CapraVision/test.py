import unittest

from gi.repository import Gtk
from gi.repository import GObject
GObject.threads_init()

import cv2
import gui, source, chain
from filters import noop

def source_image():
    image = cv2.imread('0-157.png')
    return image

def test_viewer():
    s = source.Webcam(0)
    c = chain.FilterChain()
    c.add_filter(noop)
    w = gui.WinViewer(s, c, noop)
    w.window.show_all()
    Gtk.main()
    
if __name__ == '__main__':
    test_viewer()