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

from gi.repository import Gtk

from CapraVision.client.gtk import get_ui
from CapraVision.client.gtk import tree_selected_index
from CapraVision.client.gtk import win_name

import os.path

class WinImageFolder:
    
    def __init__(self, source):
        self.source = source
        self.source.set_auto_increment(False)
        
        ui = get_ui(self, 'imageListStore')
        self.window = ui.get_object(win_name(self))
        self.txtFolder = ui.get_object('txtFolder')
        self.hscPosition = ui.get_object('hscPosition')
        self.lstImages = ui.get_object('lstImages')
        self.imageListStore = ui.get_object('imageListStore')
        
        
        if self.source.folder_name == '':
            self.open_folder()
        else:
            pos = self.source.position
            self.txtFolder.set_text(self.source.folder_name)
            self.fill_image_list(self.source.file_names)
            self.lstImages.set_cursor(pos)
            
    def fill_image_list(self, images):
        self.imageListStore.clear()
        for i in xrange(len(images)):
            self.imageListStore.append([os.path.basename(images[i])])
        if len(images) > 0:
            self.lstImages.set_cursor(0)

    def open_folder(self):
        dialog = Gtk.FileChooserDialog("Choose an image folder", None,
                                   Gtk.FileChooserAction.SELECT_FOLDER,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))    
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.txtFolder.set_text(dialog.get_filename())
            self.source.read_folder(dialog.get_filename())
            self.fill_image_list(self.source.file_names)
        dialog.destroy()

    def on_btnOpen_clicked(self, widget):
        self.open_folder()
        
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
    
    def on_btnPlay_clicked(self, widget):
        pass
    
    def on_lstImage_cursor_changed(self, widget):
        index = tree_selected_index(self.lstImages)
        if index >= 0:
            self.source.set_position(index)
            