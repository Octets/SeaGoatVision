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

from gi.repository import GObject

from CapraVision.client.gtk.utils import *

from CapraVision.core import filterchain
from CapraVision.core import mainloop

from CapraVision import imageproviders

class WinViewer():
    """Show the source after being processed by the filter fchain.
    The window receives a filter in its constructor.  
    This is the last executed filter on the source.
    """
    def __init__(self, fchain, server):
        self.source_list = imageproviders.load_sources()
        self.fchain = fchain
        self.server = server
        fchain.add_image_observer(self.chain_observer)
        fchain.add_filter_observer(self.filters_changed_observer)
        fchain.add_filter_output_observer(server.send)
        
        self.win_list = []
        self.thread = None
        self.source = None
        self.filter = None
        
        ui = get_ui(self, 'sourcesListStore', 'filterChainListStore')
        self.window = ui.get_object(win_name(self))
        self.cboFilter = ui.get_object('cboFilter')
        self.sourcesListStore = ui.get_object('sourcesListStore') 
        self.filterChainListStore = ui.get_object('filterChainListStore')
        self.imgSource = ui.get_object('imgSource')
        self.cboSource = ui.get_object('cboSource')
        
        self.sourcesListStore.append(['None'])
        for name in self.source_list.keys():
            self.sourcesListStore.append([name])
        self.fill_filters_source()
        self.cboSource.set_active(1)
        self.set_default_filter()

    def add_window_to_list(self, win):
        self.win_list.append(win.window)

    #This method is the observer of the FilterChain class.
    def chain_observer(self, filter, output):
        if filter is self.filter:
            GObject.idle_add(self.update_image, output)

    def change_source(self, new_source):
        if self.thread <> None:
            self.thread.stop()
            self.thread = None
        if self.source <> None:
            imageproviders.close_source(self.source)
        if new_source <> None:
            self.source = imageproviders.create_source(new_source)
            self.thread = mainloop.ThreadMainLoop(self.source, 1/30.0)
            self.thread.add_observer(self.thread_observer)
            self.thread.start()
        else:
            self.source = None

    def fill_filters_source(self):
        old_filter = self.filter
        count = len(self.filterChainListStore)
        
        self.filterChainListStore.clear()
        for filter in self.fchain.filters:
            self.filterChainListStore.append([filter.__class__.__name__]) 
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
                        
    def show_config(self, source):
        cls = map_source_to_ui(source)
        if cls is not None:
            win = cls(source)
            self.add_window_to_list(win)
            win.window.connect('destroy', self.on_window_destroy)
            win.window.show_all()
            
    def thread_observer(self, image):
        self.fchain.execute(image)
        
    def update_image(self, image):
        if image <> None:
            self.imgSource.set_from_pixbuf(numpy_to_pixbuf(image))
                
    def on_btnConfigure_clicked(self, widget):
        self.show_config(self.source)
        
    def on_cboSource_changed(self, widget):
        index = self.cboSource.get_active()
        source = None
        if index > 0:
            source = self.source_list[self.sourcesListStore[index][0]]
        self.change_source(source)
    
    def on_cboFilter_changed(self, widget):
        index = self.cboFilter.get_active()
        if index <> -1:
            f = self.fchain.filters[index]
            self.filter = f 
        else:
            self.filter = None

    def on_window_destroy(self, widget):
        self.win_list.remove(widget)

    def on_WinViewer_destroy(self, widget):
        self.thread.stop()
        self.fchain.remove_filter_observer(self.filters_changed_observer)
        self.fchain.remove_image_observer(self.chain_observer)
