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
import os

def get_ui(window, *names):
    ui = Gtk.Builder()
    glade_file = os.path.join('gui', 'gladefiles', win_name(window) + '.glade')
    ui.add_objects_from_file(glade_file, [win_name(window)] + 
                             [name for name in names])
    ui.connect_signals(window)
    return ui

def win_name(window):
    return window.__class__.__name__
