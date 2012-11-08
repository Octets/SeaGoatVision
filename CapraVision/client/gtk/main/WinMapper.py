#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of CapraVision.
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

import os

import cv2
import numpy as np

from gi.repository import Gtk, Gdk
import cairo

from CapraVision.client.gtk.utils import get_ui
from CapraVision.client.gtk.utils import numpy_to_pixbuf
from CapraVision.client.gtk.utils import tree_selected_index
from CapraVision.client.gtk.utils import win_name

from CapraVision.server import imageproviders

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
        
        self.image = None
        self.pixbuf_image = None
        self.surface = None
        self.color = Gdk.RGBA()
        self.color.red = 255
        self.color.green = 255
        self.color.blue = 255
        self.matrices = []
        self.undo_list = []
        self.current_index = 0
        
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
            rect.width -= ((rect.x + rect.width) - 
                           self.pixbuf_image.get_width())
        if rect.y + rect.height > self.pixbuf_image.get_height():
            rect.height -= ((rect.y + rect.height) - 
                            self.pixbuf_image.get_height())
        if rect.height < 0:
            rect.height = 0
        if rect.width < 0:
            rect.width = 0
        return rect
    
    def configure(self):
        self.configure_matrices()
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
            
    def configure_matrices(self):
        self.matrices = []
        self.matrices.append(np.zeros(
            (self.pixbuf_image.get_height(), 
             self.pixbuf_image.get_width()), np.bool))
        
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
        brush = np.ones((rect.height, rect.width), np.bool)
        self.matrices[-1] \
            [rect.y:rect.y+rect.height, rect.x:rect.x+rect.width] = brush
        
    def load_folder(self, folder):
        images = imageproviders.find_all_images(folder)
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
        f = file(self.imageListStore[self.current_index][2] + '.map', 'w')
        f.write(self.matrices[-1].tostring())
        f.close()
        
    def read_matrix_from_disk(self):
        index = tree_selected_index(self.lstImages)
        file_name = self.imageListStore[index][2] + '.map'
        if os.path.exists(file_name):
            f = file(file_name, 'r')
            s = f.read()
            f.close()
            self.matrices[-1] = np.fromstring(s, np.bool).reshape(
                                            self.pixbuf_image.get_height(), 
                                            self.pixbuf_image.get_width())
            
    def apply_matrix_to_pixbuf(self):
        for x in xrange(0, self.pixbuf_image.get_width() - 1):
            for y in xrange(0, self.pixbuf_image.get_height() - 1):
                if self.matrices[-1][y, x] == 1:
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
            self.matrices.append(np.zeros(
                            (self.pixbuf_image.get_height(), 
                            self.pixbuf_image.get_width()), np.bool))
            self.configure_surface()
            self.drwImage.queue_draw()
        
    def on_btnUndo_clicked(self, widget):
        if len(self.matrices) == 1:
            return
        matrix = self.matrices[-1]
        del self.matrices[-1]
        self.undo_list.append(matrix)
        self.configure_surface()
        self.apply_matrix_to_pixbuf()
        self.drwImage.queue_draw()

    def on_btnRedo_clicked(self, widget):
        if len(self.undo_list) == 0:
            return
        matrix = self.undo_list[-1]
        del self.undo_list[-1]
        self.matrices.append(matrix)
        self.configure_surface()
        self.apply_matrix_to_pixbuf()
        self.drwImage.queue_draw()
    
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
            self.undo_list = []
            if len(self.matrices) > 1:
                self.save_matrix_to_disk()
            self.current_index = index 
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
        _, x, y, state = event.window.get_pointer()
        if (state & Gdk.ModifierType.BUTTON1_MASK 
                and self.pixbuf_image is not None):
            self.draw(widget, x, y)    
        return True
    
    def on_drwImage_button_press_event(self, widget, event):
        if event.button == 1 and self.pixbuf_image is not None:
            self.matrices.append(self.matrices[-1].copy())
            self.undo_list = []
            self.draw(widget, event.x, event.y)
        return True
            
    def on_drwImage_button_release_event(self, widget, event):
        pass
