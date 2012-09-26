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

from gi.repository import Gtk, Gdk, GObject, GdkPixbuf
import cairo

import cv2
import numpy as np
import os
import threading

from guifilter import map_filter_to_ui
from utils import *

import chain
import sources
import filters

class WinFilterChain:
    """Main window
    Allow the user to create, edit and test filter chains
    """
    
    WINDOW_TITLE = "Capra Vision"

    def __init__(self):
        ui = get_ui(self, 'filterChainListStore', 
                    'imgOpen', 'imgNew', 'imgUp', 'imgDown')
        self.window = ui.get_object(win_name(self))
        self.lstFilters = ui.get_object('lstFilters')
        self.btnView = ui.get_object('btnView')
        self.btnAdd = ui.get_object('btnAdd')
        self.btnRemove = ui.get_object('btnRemove')
        self.btnConfig = ui.get_object('btnConfig')
        self.btnUp = ui.get_object('btnUp')
        self.btnDown = ui.get_object('btnDown')
        self.txtFilterChain = ui.get_object('txtFilterChain')
        
        self.win_list = []
        
        self.filterChainListStore = ui.get_object('filterChainListStore')
        self.set_state_empty()
        self.change_state()

    def add_window_to_list(self, win):
        self.win_list.append(win.window)
        
    def change_state(self):
        tools_enabled = self.state <> WindowState.Empty
        self.btnAdd.set_sensitive(tools_enabled)
        self.btnConfig.set_sensitive(tools_enabled)
        self.btnDown.set_sensitive(tools_enabled)
        self.btnRemove.set_sensitive(tools_enabled)
        self.btnUp.set_sensitive(tools_enabled)
        self.btnView.set_sensitive(tools_enabled)

    def del_current_row(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        self.chain.remove_filter(self.selected_filter())
        
    def filter_modif_callback(self):
        self.set_state_modified()
        
    def filters_changed_observer(self):
        self.show_filter_chain()

    def is_state_modified_or_created(self):
        return (self.state == WindowState.Create or
            self.state == WindowState.Modified)

    def msg_confirm_create_new(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   Gtk.ButtonsType.YES_NO, 
                                   "Create new filterchain?")
        result = dialog.run()
        dialog.destroy()
        return result
        
    def msg_confirm_save_before_closing(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   None, 
                                   "Save changes?")
        dialog.add_button('Close without saving', Gtk.ResponseType.CLOSE)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        dialog.format_secondary_text(
            "Do you want to save the current filterchain before closing?")
        result = dialog.run()
        dialog.destroy()
        return result
    
    def msg_confirm_save_before_new(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   None, 
                                   "Save changes?")
        dialog.add_button(Gtk.STOCK_NO, Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_YES, Gtk.ResponseType.YES)
        dialog.format_secondary_text(
            "Do you want to save the current filterchain before proceeding?")
        result = dialog.run()
        dialog.destroy()
        return result

    def msg_warn_del_row(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                            Gtk.ButtonsType.YES_NO, "Delete selected filter")
        dialog.format_secondary_text(
                                "Do you want to remove the selected filter?")
        result = dialog.run()
        dialog.destroy()
        return result

    def save_chain(self):
        if self.state == WindowState.Empty:
            return True
        elif self.state == WindowState.Create:
            return self.save_chain_as()
        else:
            chain.write(self.txtFilterChain.get_text(), self.chain)
            self.set_state_show()
            return True

    def save_chain_as(self):
        if self.state == WindowState.Empty:
            return True
        dialog = Gtk.FileChooserDialog("Save filterchain", None,
                                   Gtk.FileChooserAction.SAVE,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = dialog.run()
        fname = dialog.get_filename()
        dialog.destroy()

        if not fname.endswith('.filterchain'):
            fname += '.filterchain'

        if response == Gtk.ResponseType.OK:
            chain.write(fname, self.chain)
            self.txtFilterChain.set_text(fname)
            self.set_state_show()
            return True
        else:
            return False

    def selected_filter(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        if iter is None:
            return None
        path = model.get_path(iter)
        return self.chain.filters[path.get_indices()[0]]
    
    def set_state_create(self):
        self.state = WindowState.Create
        self.window.set_title(self.WINDOW_TITLE + " *")
        self.txtFilterChain.set_text('<new>')
        self.change_state()

    def set_state_empty(self):
        self.state = WindowState.Empty
        self.window.set_title(self.WINDOW_TITLE)
        self.change_state()

    def set_state_modified(self):
        if self.state <> WindowState.Create:
            self.state = WindowState.Modified
            self.window.set_title(self.WINDOW_TITLE + " *")
            self.change_state()
                            
    def set_state_show(self):
        self.state = WindowState.Show
        self.window.set_title(self.WINDOW_TITLE)
        self.change_state()

    def show_config(self, filter):
        cls = map_filter_to_ui(filter)
        if cls is not None:
            win = cls(filter, self.filter_modif_callback)
            self.add_window_to_list(win)
            win.window.connect('destroy', self.on_window_destroy)
            win.window.show_all()
    
    def show_filter_chain(self):
        self.filterChainListStore.clear()
        for filter in self.chain.filters:
            self.filterChainListStore.append(
                        [filter.__class__.__name__, filter.__doc__]) 

    def use_new_chain(self, chain):
        if chain is None:
            return
        for win in list(self.win_list):
            win.destroy()
        self.chain = chain
        self.chain.add_filter_observer(self.filters_changed_observer)
        self.show_filter_chain()
                                                                                    
    def on_btnNew_clicked(self, widget):
        if self.state == WindowState.Show:
            if self.msg_confirm_create_new() == Gtk.ResponseType.NO:
                return
        elif self.is_state_modified_or_created():
            result = self.msg_confirm_save_before_new()
            if result == Gtk.ResponseType.YES:
                pass
            elif result == Gtk.ResponseType.CANCEL:
                return
        self.use_new_chain(chain.FilterChain())
        self.set_state_create()

    def on_btnOpen_clicked(self, widget):
        if self.is_state_modified_or_created():
            result = self.msg_confirm_save_before_new()
            if result == Gtk.ResponseType.YES:
                pass
            elif result == Gtk.ResponseType.CANCEL:
                return

        dialog = Gtk.FileChooserDialog("Choose a filterchain file", None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
        ff = Gtk.FileFilter()
        ff.set_name('Filterchain')
        ff.add_pattern('*.filterchain')
    
        dialog.set_filter(ff)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            c = chain.read(dialog.get_filename())
            if c is not None:
                self.use_new_chain(c)
                self.txtFilterChain.set_text(dialog.get_filename())
                self.set_state_show()
        dialog.destroy()
            
    def on_btnSave_clicked(self, widget):
        self.save_chain()
        
    def on_btnSaveAs_clicked(self, widget):
        self.save_chain_as()

    def on_btnView_clicked(self, widget):
        win = WinViewer(self.chain)
        win.window.connect('destroy', self.on_window_destroy)
        self.add_window_to_list(win)
        win.window.show_all()

    def on_btnAdd_clicked(self, widget):
        win = WinFilterSel()
        if win.window.run() == Gtk.ResponseType.OK:
            self.chain.add_filter(win.selected_filter())
            self.set_state_modified()
        win.window.destroy()
            
    def on_btnRemove_clicked(self, widget):
        if (tree_row_selected(self.lstFilters) and 
                            self.msg_warn_del_row() == Gtk.ResponseType.YES):
            self.del_current_row()
                    
    def on_btnConfig_clicked(self, widget):
        if tree_row_selected(self.lstFilters):
            self.show_config(self.selected_filter())
                    
    def on_btnUp_clicked(self, widget):
        filter = self.selected_filter()
        if filter is not None:
            index = utils.tree_selected_index(self.lstFilters)
            if index > 0:
                self.chain.move_filter_up(filter)
                self.lstFilters.set_cursor(index - 1)
    
    def on_btnDown_clicked(self, widget):
        filter = self.selected_filter()
        if filter is not None:
            index = tree_selected_index(self.lstFilters)
            if index < len(self.chain.filters) - 1:
                self.chain.move_filter_down(filter)
                self.lstFilters.set_cursor(index + 1)
                    
    def on_lstFilters_button_press_event(self, widget, event):
        if event.get_click_count()[1] == 2L:
            self.show_config(self.selected_filter())

    def on_window_destroy(self, widget):
        self.win_list.remove(widget)

    def on_WinFilterChain_delete_event(self, widget, data=None):
        if self.is_state_modified_or_created():
            result = self.msg_confirm_save_before_closing()
            if result == Gtk.ResponseType.OK:
                if self.save_chain():
                    Gtk.main_quit()
            elif result == Gtk.ResponseType.CANCEL:
                return True
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

    #This method is the observer of the FilterChain class.
    def chain_observer(self, filter, output):
        if filter is self.filter:
            GObject.idle_add(self.update_image, output)

    def change_source(self, new_source):
        if self.thread <> None:
            self.thread.stop()
            self.thread = None
        if self.source <> None:
            sources.close_source(self.source)
        if new_source <> None:
            self.source = sources.create_source(new_source)
            self.thread = chain.ThreadMainLoop(self.source, 1/30.0)
            self.thread.add_observer(self.thread_observer)
            self.thread.start()
        else:
            self.source = None

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
            
    def filters_changed_observer(self):
        self.fill_filters_source()

    def set_default_filter(self):
        if len(self.chain.filters) > 0:
            self.filter = self.chain.filters[-1]
            self.cboFilter.set_active(len(self.chain.filters)-1)
                                
    def thread_observer(self, image):
        self.chain.execute(image)
        
    def update_image(self, image):
        if image <> None:
            self.imgSource.set_from_pixbuf(numpy_to_pixbuf(image))
                
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

    def on_WinViewer_destroy(self, widget):
        self.thread.stop()
        self.chain.remove_filter_observer(self.filters_changed_observer)
        self.chain.remove_image_observer(self.chain_observer)
        
class WinMapper:
    """Tool to identify lines in images
        Drawing code adapted from gtk demo drawingarea.py
    """
    
    def __init__(self):
        ui = get_ui(self, 'imageListStore', 'adjSize')
        self.window = ui.get_object(win_name(self))
        self.imageListStore = ui.get_object('imageListStore') 
        self.txtFolder = ui.get_object('txtFolder')
        self.lstImages = ui.get_object('lstImages')
        self.drwImage = ui.get_object('drwImage')
        self.spnSize = ui.get_object('spnSize')
        self.spnSize.set_value(16)
        
        self.drwImage.set_events(self.drwImage.get_events()
                      | Gdk.EventMask.LEAVE_NOTIFY_MASK
                      | Gdk.EventMask.BUTTON_PRESS_MASK
                      | Gdk.EventMask.BUTTON_RELEASE_MASK
                      | Gdk.EventMask.POINTER_MOTION_MASK
                      | Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        
        self.pixbuf_image = None
        self.surface = None
        self.color = Gdk.RGBA()
        self.color.red = 255
        self.color.green = 255
        self.color.blue = 255
        self.matrix = None
        
    def brush_size(self, x, y, size):
        rect = Gdk.Rectangle()
        rect.x = x - size / 2
        rect.y = y - size / 2
        rect.width = size
        rect.height = size
        
        if rect.x < 0:
            rect.width += rect.x
            rect.x = 0
        if rect.y < 0:
            rect.height += rect.y
            rect.y = 0
        if rect.x + rect.width > self.pixbuf_image.get_width():
            rect.width -= ((rect.x + rect.width) - self.pixbuf_image.get_width())
        if rect.y + rect.height > self.pixbuf_image.get_height():
            rect.height -= ((rect.y + rect.height) - self.pixbuf_image.get_height())
        if rect.height < 0:
            rect.height = 0
        if rect.width < 0:
            rect.width = 0
        return rect
    
    def configure(self):
        self.configure_matrix()
        self.configure_surface()
        self.read_matrix_from_disk()
        self.apply_matrix_to_pixbuf()
        
    def configure_surface(self):
        self.surface = self.drwImage.get_window().create_similar_surface(
                                                    cairo.CONTENT_COLOR_ALPHA,
                                                    self.pixbuf_image.get_width(),
                                                    self.pixbuf_image.get_height())
        context = cairo.Context(self.surface)
        context.set_source_rgba(0, 0, 0, 0)
        context.paint()
            
    def configure_matrix(self):
        self.matrix = np.zeros(
            (self.pixbuf_image.get_height(), self.pixbuf_image.get_width()), np.uint8)
        
    def draw(self, widget, x, y):
        self.draw_brush(widget, x, y, self.spnSize.get_value_as_int())
        self.draw_matrix(x, y, self.spnSize.get_value_as_int())
        
    def draw_brush(self, widget, x, y, size):
        rect = self.brush_size(x, y, size)
        context = cairo.Context(self.surface)
        context.set_source_rgba(
                                self.color.red, 
                                self.color.green, 
                                self.color.blue, 1)

        Gdk.cairo_rectangle(context, rect)
        context.fill()

        widget.get_window().invalidate_rect(rect, False)
        
    def draw_matrix(self, x, y, size):
        rect = self.brush_size(x, y, size)
        brush = np.ones((rect.height, rect.width), np.uint8)
        self.matrix[rect.y:rect.y+rect.height, rect.x:rect.x+rect.width] = brush
        
    def load_folder(self, folder):
        images = sources.find_all_images(folder)
        self.imageListStore.clear()
        for image in images:
            self.imageListStore.append([os.path.exists(image + '.map'), 
                                        os.path.basename(image),
                                        image,
                                        None])
        if len(images) > 0:
            self.lstImages.set_cursor(0)
        
    def msg_confirm_clear(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   Gtk.ButtonsType.YES_NO, 
                                   "Clear picture?")
        result = dialog.run()
        dialog.destroy()
        return result
            
    def save_matrix_to_disk(self):
        index = tree_selected_index(self.lstImages)
        f = file(self.imageListStore[index][2] + '.map', 'w')
        f.write(self.matrix.tostring())
        f.close()
        
    def read_matrix_from_disk(self):
        index = tree_selected_index(self.lstImages)
        file_name = self.imageListStore[index][2] + '.map'
        if os.path.exists(file_name):
            f = file(file_name, 'r')
            s = f.read()
            f.close()
            self.matrix = np.fromstring(s, np.uint8)
        
    def apply_matrix_to_pixbuf(self):
        for x in range(0, self.pixbuf_image.get_width() - 1):
            for y in range(0, self.pixbuf_image.get_height() - 1):
                if self.matrix[y, x] == 1:
                    self.draw_brush(self.drwImage, x, y, 1)
                    
    def on_btnOpen_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Choose an image folder", None,
                                   Gtk.FileChooserAction.SELECT_FOLDER,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
    
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            folder = dialog.get_filename()
            self.txtFolder.set_text(folder)
            if folder is not None:
                self.load_folder(folder)
        dialog.destroy()
    
    def on_btnFirst_clicked(self, widget):
        self.lstImages.set_cursor(0)
    
    def on_btnPrevious_clicked(self, widget):
        position = tree_selected_index(self.lstImages) - 1
        if position >= 0:
            self.lstImages.set_cursor(position)
    
    def on_btnNext_clicked(self, widget):
        position = tree_selected_index(self.lstImages) + 1
        if position < len(self.imageListStore):
            self.lstImages.set_cursor(position)
    
    def on_btnLast_clicked(self, widget):
        position = len(self.imageListStore) - 1
        self.lstImages.set_cursor(position)
    
    def on_btnClear_clicked(self, widget):
        if self.msg_confirm_clear() == Gtk.ResponseType.YES:
            self.configure_matrix()
            self.apply_matrix_to_pixbuf()
        
    def on_btnUndo_clicked(self, widget):
        pass
    
    def on_btnRedo_clicked(self, widget):
        pass
    
    def on_btnColor_clicked(self, widget):
        dialog = Gtk.ColorChooserDialog("Please choose a color")
        dialog.set_rgba(self.color)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.get_rgba(self.color)
        dialog.destroy()
        
    def on_spnSize_change_value(self, widget):
        pass
    
    def on_lstImages_cursor_changed(self, widget):
        index = tree_selected_index(self.lstImages)
        if index >= 0:
            img = cv2.imread(self.imageListStore[index][2])
            self.pixbuf_image = numpy_to_pixbuf(img)
            self.drwImage.set_size_request(img.shape[1], img.shape[0])
            self.drwImage.queue_draw()
            self.configure()
                
    def on_drwImage_draw_image(self, widget, context):
        if self.pixbuf_image is not None:
            Gdk.cairo_set_source_pixbuf(context, self.pixbuf_image, 0, 0)
            context.paint()
        return False

    def on_drwImage_draw_lines(self, widget, context):
        if self.pixbuf_image is not None:
            context.set_source_surface(self.surface, 0, 0)
            context.paint()
        return True
    
    def on_drwImage_motion_notify_event(self, widget, event):
        (window, x, y, state) = event.window.get_pointer()
        if (state & Gdk.ModifierType.BUTTON1_MASK 
                and self.pixbuf_image is not None):
            self.draw(widget, x, y)    
        return True
    
    def on_drwImage_button_press_event(self, widget, event):
        if event.button == 1 and self.pixbuf_image is not None:
            self.draw(widget, event.x, event.y)
        return True
            
    def on_drwImage_button_release_event(self, widget, event):
        if event.button == 1 and self.matrix is not None:
            self.save_matrix_to_disk()
    
