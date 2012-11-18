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

import cv2

from gi.repository import GObject

from CapraVision.client.gtk import get_ui
from CapraVision.client.gtk import numpy_to_pixbuf
from CapraVision.client.gtk import win_name

class WinViewer():
    """Show the source after being processed by the filterchain.
    The window receives a filter in its constructor.  
    This is the last executed filter on the source.
    """
    def __init__(self, fchain, server, thread):
        self.fchain = fchain
        self.server = server
        fchain.add_image_observer(self.chain_observer)
        fchain.add_filter_observer(self.filters_changed_observer)
        fchain.add_filter_output_observer(server.send)
        
        self.win_list = []
        self.thread = thread
        self.thread.add_observer(self.thread_observer)

        self.filter = None
        self.size = 1.0
        self.image_shape = (320, 240, 0)
        
        ui = get_ui(self, 'sourcesListStore', 
                    'filterChainListStore', 
                    'sizeListStore')
        
        self.window = ui.get_object(win_name(self))
        self.cboFilter = ui.get_object('cboFilter')
        self.filterChainListStore = ui.get_object('filterChainListStore')
        self.sizeListStore = ui.get_object('sizeListStore')
        self.imgSource = ui.get_object('imgSource')
        self.scwImage = ui.get_object('scwImage')
        self.vptImage = ui.get_object('vptImage')
        self.spnSize = ui.get_object('spnSize')
        self.cboSize = ui.get_object('cboSize')
        self.cboSize.set_active(5) # 100%
        
        self.fill_filters_source()
        self.set_default_filter()

    def add_window_to_list(self, win):
        self.win_list.append(win.window)

    #This method is the observer of the FilterChain class.
    def chain_observer(self, filtre, output):
        if filtre is self.filter:
            GObject.idle_add(self.update_image, output)

    def change_display_size(self):
        index = self.cboSize.get_active()
        if index > 0:
            new_size = self.sizeListStore[index][1] / 100.0
            height, width, _ = self.image_shape
            width = width * new_size
            height = height * new_size
            self.window.resize(10, 10)
            if width <= 640 and height <= 480:
                self.scwImage.set_size_request(width + 16, height + 16)
            else:
                self.scwImage.set_size_request(640 + 16, 480 + 16)
                
            self.size = new_size

    def fill_filters_source(self):
        old_filter = self.filter
        count = len(self.filterChainListStore)
        
        self.filterChainListStore.clear()
        for filtre in self.fchain.filters:
            self.filterChainListStore.append([filtre.__class__.__name__]) 
        if (old_filter is not None and 
                            old_filter in self.fchain.filters and 
                            count >= len(self.filterChainListStore)):
            self.cboFilter.set_active(self.fchain.filters.index(old_filter))
        else:
            self.set_default_filter()
            
    def filters_changed_observer(self):
        self.fill_filters_source()

    def set_default_filter(self):
        if len(self.fchain.filters) > 0:
            self.filter = self.fchain.filters[-1]
            self.cboFilter.set_active(len(self.fchain.filters)-1)
                                    
    def thread_observer(self, image):
        self.fchain.execute(image)
        
    def update_image(self, image):
        if image <> None:
            if self.image_shape <> image.shape:
                self.image_shape = image.shape
                self.change_display_size()
            if self.size <> 1.0:
                image = cv2.resize(image, 
                    (int(image.shape[1] * self.size), 
                     int(image.shape[0] * self.size)))
            self.imgSource.set_from_pixbuf(numpy_to_pixbuf(image))
                            
    def on_cboFilter_changed(self, widget):
        index = self.cboFilter.get_active()
        if index <> -1:
            f = self.fchain.filters[index]
            self.filter = f 
        else:
            self.filter = None

    def on_cboSize_changed(self, widget):
        self.change_display_size()
                
    def on_window_destroy(self, widget):
        self.win_list.remove(widget)

    def on_WinViewer_destroy(self, widget):
        self.thread.remove_observer(self.thread_observer)
        self.fchain.remove_filter_observer(self.filters_changed_observer)
        self.fchain.remove_image_observer(self.chain_observer)
