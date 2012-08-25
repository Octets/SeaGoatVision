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

from gi.repository import Gtk, GObject, GdkPixbuf

import cv2
import tempfile
import threading

from filters.implementation import BGR2RGB
from guifilter import map_filter_to_ui
from utils import get_ui, win_name

import chain
import sources
import filters

bgr2rgb = BGR2RGB()

class WinFilterChain:
    """Main window
    Allow the user to create, edit and test filter chains
    """
    def __init__(self):
        ui = get_ui(self, 'filterChainListStore', 
                    'imgOpen', 'imgNew', 'imgUp', 'imgDown')
        self.window = ui.get_object(win_name(self))
        self.lstFilters = ui.get_object('lstFilters')
        self.chain = chain.FilterChain()
        self.filterChainListStore = ui.get_object('filterChainListStore')
        self.init_window()
        
    def init_window(self):
        pass
    
    def add_filter(self, filter):
        self.chain.add_filter(filter())
        self.show_filter_chain()
    
    def show_filter_chain(self):
        self.filterChainListStore.clear()
        for filter in self.chain.filters:
            self.filterChainListStore.append(
                        [filter.__class__.__name__, filter.__doc__]) 
    
    def row_selected(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        return iter is not None

    def selected_filter(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        if iter is None:
            return None
        path = model.get_path(iter)
        return self.chain.filters[path.get_indices()[0]]
    
    def del_current_row(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        self.chain.remove_filter(self.selected_filter())
        del self.filterChainListStore[iter]
        
    def msg_warn_del_row(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.QUESTION, 
                                   Gtk.ButtonsType.YES_NO, "Question")
        dialog.format_secondary_text(
                                "Do you want to remove the selected filter?")
        result = dialog.run()
        dialog.destroy()
        return result
            
    def on_btnOpen_clicked(self, widget):
        pass
    
    def on_btnNew_clicked(self, widget):
        pass
    
    def on_btnSource_clicked(self, widget):
        pass
    
    def on_btnAdd_clicked(self, widget):
        win = WinFilterSel()
        if win.window.run() == Gtk.ResponseType.OK:
            self.add_filter(win.selected_filter)
        win.window.destroy()
            
    def on_btnRemove_clicked(self, widget):
        if (self.row_selected() and 
                            self.msg_warn_del_row() == Gtk.ResponseType.YES):
            self.del_current_row()
                    
    def on_btnConfig_clicked(self, widget):
        if self.row_selected():
            filter = self.selected_filter()
            cls = map_filter_to_ui(filter)
            if cls is not None:
                win = cls(filter)
                win.window.show_all()
    
    def on_btnView_clicked(self, widget):
        win = WinViewer(self.chain)
        win.window.show_all()
        
    def on_btnUp_clicked(self, widget):
        pass
    
    def on_dtnDown_clicked(self, widget):
        pass
    
    def on_btnSave_clicked(self, widget):
        pass

    def on_btnCancel_clicked(self, widget):
        pass
    
    def on_btnQuit_clicked(self, widget):
        pass
    
    def on_btnClear_clicked(self, widget):
        pass
    
    def on_cboSource_changed(self, widget):
        pass
    
    def on_winFilterChain_destroy(self, widget):
        Gtk.main_quit()
      
class WinFilterSel:
    """Allow the user to select a filter to add to the filterchain"""
    
    def __init__(self):
        self.filter_list = filters.load_filters()
        ui = get_ui(self, 'filtersListStore')
        self.window = ui.get_object(win_name(self))
        self.filtersListStore = ui.get_object('filtersListStore')
        self.lstFilters = ui.get_object('lstFilters')

        self.window.set_modal(True)
        for name, filter in self.filter_list.items():
            self.filtersListStore.append([name, filter.__doc__])
        self.filtersListStore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        
        self.selected_filter = None
        
    def get_selected_filter(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        filter_name = self.filtersListStore.get_value(iter, 0)
        return self.filter_list[filter_name]
    
    def on_btnOK_clicked(self, widget):
        self.selected_filter = self.get_selected_filter()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.window.destroy()
    
    def on_lstFilters_button_press_event(self, widget, event):
        if event.get_click_count()[1] == 2L:
            self.selected_filter = self.get_selected_filter()
            self.window.response(Gtk.ResponseType.OK)
            self.window.destroy()
                
class WinViewer():
    """Show the source after being processed by the filter chain.
    The window receives a filter in its constructor.  
    This is the last executed filter on the source.
    """
    def __init__(self, filterchain):
        self.source_list = sources.load_sources()
        self.chain = filterchain
        filterchain.add_image_observer(self.chain_observer)
        filterchain.add_filter_observer(self.filters_changed_observer)
        
        self.thread = None
        self.source = None
        self.filter = None
        
        self.temp_file = tempfile.mktemp('.jpg')

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

    def fill_filters_source(self):
        old_filter = self.filter
        count = len(self.filterChainListStore)
        
        self.filterChainListStore.clear()
        for filter in self.chain.filters:
            self.filterChainListStore.append([filter.__class__.__name__]) 
        if (old_filter is not None and 
                            old_filter in self.chain.filters and 
                            count >= len(self.filterChainListStore)):
            self.cboFilter.set_active(self.chain.filters.index(old_filter))
        else:
            self.set_default_filter()
            
    def set_default_filter(self):
        if len(self.chain.filters) > 0:
            self.filter = self.chain.filters[-1]
            self.cboFilter.set_active(len(self.chain.filters)-1)
        
    def change_source(self, new_source):
        if self.thread <> None:
            self.thread.stop()
            self.thread = None
        if self.source <> None:
            sources.close_source(self.source)
        if new_source <> None:
            self.source = sources.create_source(new_source)
            self.thread = chain.ThreadMainLoop(self.source, self.chain, 1/60)
            self.thread.start()
        else:
            self.source = None
        
    #This method is the observer of the FilterChain class.
    def chain_observer(self, filter, output):
        if filter is self.filter:
            GObject.idle_add(self.update_image3, output)
        
    def filters_changed_observer(self):
        self.fill_filters_source()
        
    def update_image(self, image):
        if image <> None:
            image = bgr2rgb.execute(image)
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(image, 
                                                    GdkPixbuf.Colorspace.RGB, 8)
            self.imgSource.set_from_pixbuf(pixbuf)

    # fix for GTK3 because https://bugzilla.gnome.org/show_bug.cgi?id=674691
    # To overcome this bug, the image is saved to a file in the temp folder.
    # The image is then reloaded in the window.
    def update_image3(self, image):
        if image <> None:
            cv2.imwrite(self.temp_file, image)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.temp_file)
            self.imgSource.set_from_pixbuf(pixbuf)
        
    def on_WinViewer_destroy(self, widget):
        self.thread.stop()
        
    def on_btnConfigure_clicked(self, widget):
        pass
    
    def on_cboSource_changed(self, widget):
        index = self.cboSource.get_active()
        source = None
        if index > 0:
            source = self.source_list[self.sourcesListStore[index][0]]
        self.change_source(source)
    
    def on_cboFilter_changed(self, widget):
        index = self.cboFilter.get_active()
        if index <> -1:
            f = self.chain.filters[index]
            self.filter = f 
        else:
            self.filter = None
        