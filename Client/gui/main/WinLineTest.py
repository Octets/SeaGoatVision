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

from gui.utils import *

from gi.repository import Gtk

import cv2
import numpy as np

from CapraVision import sources
from CapraVision.tests.line_test import LineTest

class WinLineTest:
    
    def __init__(self):
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.txtFilterchain = ui.get_object('txtFilterchain')
        self.txtTestFolder = ui.get_object('txtTestFolder')
        self.lblPrecision = ui.get_object('lblPrecision')
        self.lblNoise = ui.get_object('lblNoise')
        self.lblNbImages = ui.get_object('lblNbImages')
        
        self.test = None
        
    def init_window(self):
        pass
    
    def msg_on_no_filterchain(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, 
                                   Gtk.ButtonsType.OK, 
                                   "You must select a filterchain file.")
        result = dialog.run()
        dialog.destroy()
        return result
    
    def msg_on_no_test_folder(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, 
                                   Gtk.ButtonsType.OK, 
                                   "You must select a test folder.")
        result = dialog.run()
        dialog.destroy()
        return result
    
    def msg_on_no_test_images(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, 
                            Gtk.ButtonsType.OK, 
                            "There are no image map files in the test folder.")
        result = dialog.run()
        dialog.destroy()
        return result
    
    def on_btnOK_clicked(self, widget):
        folder = self.txtTestFolder.get_text()
        filterchain = self.txtFilterchain.get_text()
        if folder == '':
            self.msg_on_no_test_folder()
            return
        elif filterchain == '':
            self.msg_on_no_filterchain()
            return
        
        test = LineTest(folder, filterchain)
        image_number = test.total_images()
        if image_number == 0:
            self.msg_on_no_test_images()
            return
        self.lblNbImages.set_text(str(image_number))
        test.launch()
        noise = str(round(test.avg_noise() * 100.0, 2)) + '%'
        self.lblNoise.set_text(noise)
        precision = str(round(test.avg_precision() * 100.0, 2)) + '%'
        self.lblPrecision.set_text(precision)
        
    def on_btnClear_clicked(self, widget):
        self.txtFilterchain.set_text('')
        self.txtTestFolder.set_text('')
        self.lblNoise.set_text('0%')
        self.lblPrecision.set_text('0%')
        self.lblNbImages.set_text('0')
        
    def on_btnOpenFilterchain_clicked(self, widget):
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
            self.txtFilterchain.set_text(dialog.get_filename())
        dialog.destroy()

    
    def on_btnOpenTestFolder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Choose an image folder", None,
                                   Gtk.FileChooserAction.SELECT_FOLDER,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))    
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.txtTestFolder.set_text(dialog.get_filename())
        dialog.destroy()

    