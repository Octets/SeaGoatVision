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
from CapraVision.server.imageproviders.utils import supported_image_formats

class WinSingleImage(Gtk.Window):
    
    def __init__(self, source):
        Gtk.Window.__init__(self)
        
        self.source = source
        
        self.dialog = Gtk.FileChooserDialog("Choose an image file", None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
        ff = Gtk.FileFilter()
        ff.set_name("Images")
        for format in supported_image_formats():
            ff.add_pattern("*%(ext)s" % {"ext" : format})
        self.dialog.set_filter(ff)

        self.window = self
        
    def show_all(self):
        response = self.dialog.run()

        if response == Gtk.ResponseType.OK:
            self.source.set_image(self.dialog.get_filename())
            
        self.dialog.destroy()
        self.destroy()
        