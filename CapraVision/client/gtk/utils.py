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

from gi.repository import Gtk, GdkPixbuf
import Image

import os
import StringIO

from CapraVision.server.filters.implementation.channels.bgr2rgb import BGR2RGB

def tree_selected_index(treeview):
    sel = treeview.get_selection()
    if sel is None:
        return -1
    (model, iterator) = sel.get_selected()
    if iterator is None:
        return -1
    path = model.get_path(iterator)
    return path.get_indices()[0]

def tree_row_selected(treeview):
    _, iterator = treeview.get_selection().get_selected()
    return iterator is not None

def numpy_to_pixbuf(image):
    bgr2rgb = BGR2RGB()
    image = bgr2rgb.execute(image)
    img = Image.fromarray(image)
    buff = StringIO.StringIO()
    img.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader()
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()
    return pixbuf

def get_ui(window, *names):
    ui = Gtk.Builder()
    glade_file = os.path.join('CapraVision', 'client', 'gtk', 'gladefiles',
                              win_name(window) + '.glade')
    ui.add_objects_from_file(glade_file, [win_name(window)] +
                             [name for name in names])
    ui.connect_signals(window)
    return ui

def win_name(window):
    return window.__class__.__name__

class WindowState:
    """Enumeration for the main window state
        Empty = No file to edit
        CreateNew = User created a new filter chain
        ShowExisting = User opened a file and he did not modify anything yet
        ExistingModified = File exists and the user made modifications
    """
    Empty, Create, Show, Modified = range(4)

