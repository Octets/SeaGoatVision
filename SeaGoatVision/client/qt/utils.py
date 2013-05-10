#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
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

from PySide import QtUiTools
from PySide import QtCore
import Image
import ImageQt

import inspect
import os

from filters.public.bgr2rgb import BGR2RGB

def tree_selected_index(treeview):
    (model, iter) = treeview.get_selection().get_selected()
    if iter is None:
        return -1
    path = model.get_path(iter)
    return path.get_indices()[0]

def tree_row_selected(treeview):
    (model, iter) = treeview.get_selection().get_selected()
    return iter is not None

def numpy_to_imageQt(image):
    bgr2rgb = BGR2RGB()
    image = bgr2rgb.execute(image)
    img = Image.fromarray(image)
    imageQt = ImageQt.ImageQt(img)
    """ buff = StringIO.StringIO()
    img.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader()
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()"""
    return imageQt

def get_ui(widget):
    loader = QtUiTools.QUiLoader()
    uiPath = os.path.join('SeaGoatVision', 'client', 'qt', 'uifiles', win_name(widget) + '.ui')
    print uiPath
    uiFile = QtCore.QFile(uiPath)
    uiFile.open(QtCore.QFile.ReadOnly)
    return loader.load(uiFile)

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
