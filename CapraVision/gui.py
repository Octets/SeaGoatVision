#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of CapraVision.
#    
#    CapraVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on 2012-07-23

@author: Benoit Paquet
'''

from gi.repository import Gtk, GObject, GdkPixbuf
import cv2
import tempfile
import threading

import chain
from filters import bgr_to_rgb

def get_ui(window, *names):
    ui = Gtk.Builder()
    ui.add_objects_from_file('gui.glade', [name for name in names])
    ui.connect_signals(window)
    return ui

class WinFilterChain:
    
    def __init__(self):
        ui = get_ui(self, 'winFilterChain', 'filtersListStore', 'sourcesListStore')
        self.window = ui.get_object('winFilterChain')
        self.chain = chain.FilterChain()
    
    def init_window(self):
        pass
    
    def on_btnOpen_clicked(self, widget):
        pass
    
    def on_btnSource_clicked(self, widget):
        pass
    
    def on_btnAdd_clicked(self, widget):
        pass
    
    def on_btnRemove_clicked(self, widget):
        pass
    
    def on_btnConfig_clicked(self, widget):
        pass
    
    def on_btnView_clicked(self, widget):
        pass
    
    def on_btnCreate_clicked(self, widget):
        pass
    
    def on_btnSave_clicked(self, widget):
        pass

    def on_btnSaveAs_clicked(self, widget):
        pass
    
    def on_btnCancel_clicked(self, widget):
        pass
    
    def on_btnQuit_clicked(self, widget):
        pass
    
    def on_cboSource_changed(self, widget):
        pass
    
class WinViewer():
    
    def __init__(self, source, filterchain, filter):
        ui = get_ui(self, 'winViewer')
        self.window = ui.get_object('winViewer')
        self.imgSource = ui.get_object('imgSource')
        self.source = source
        self.chain = filterchain
        self.filter = filter
        filterchain.add_observer(self.chain_observer)
        self.temp_file = tempfile.mktemp('.jpg')
        self.window.set_title(filter.__name__)
        self.thread = chain.ThreadMainLoop(source, filterchain, 0)
        self.thread.start()

    def chain_observer(self, filter, output):
        if filter.__name__ == self.filter.__name__:
            GObject.idle_add(self.update_image3, output)
            return
        
    def update_image(self, image):
        image = bgr_to_rgb(image)
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(image, GdkPixbuf.Colorspace.RGB, 8)
        self.imgSource.set_from_pixbuf(pixbuf)

    # fix for GTK3 because https://bugzilla.gnome.org/show_bug.cgi?id=674691
    def update_image3(self, image):
        cv2.imwrite(self.temp_file, image)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.temp_file)
        self.imgSource.set_from_pixbuf(pixbuf)
        
    def on_winViewer_destroy(self, widget):
        self.thread.stop()
        
    def on_btnConfigure_clicked(self, widget):
        pass
    
    def on_cboSource_changed(self, widget):
        pass
    