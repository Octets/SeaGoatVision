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

import copy
from gui.utils import *

class WinColorLevel:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.hscRed = ui.get_object('hscRed')
        self.hscGreen = ui.get_object('hscGreen')
        self.hscBlue = ui.get_object('hscBlue')
        self.init_window()
        
    def init_window(self):
        self.hscRed.set_range(0, 100)
        self.hscRed.set_value(self.filtre.red)
        self.hscGreen.set_range(0, 100)
        self.hscGreen.set_value(self.filtre.green)
        self.hscBlue.set_range(0, 100)
        self.hscBlue.set_value(self.filtre.blue)
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.red = self.filtre_init.red
        self.filtre.green = self.filtre_init.green
        self.filtre.blue = self.filtre_init.blue
        self.init_window()
        
    def on_hscRed_value_changed(self, widget):
        self.filtre.red = self.hscRed.get_value()
        
    def on_hscGreen_value_changed(self, widget):
        self.filtre.green = self.hscGreen.get_value()

    def on_hscBlue_value_changed(self, widget):
        self.filtre.blue = self.hscBlue.get_value()
