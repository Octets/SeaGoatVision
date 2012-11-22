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

from CapraVision.client.gtk import get_ui
from CapraVision.client.gtk import win_name

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
        self.hscRed.set_value(self.filtre.get_red())
        self.hscGreen.set_range(0, 100)
        self.hscGreen.set_value(self.filtre.get_green())
        self.hscBlue.set_range(0, 100)
        self.hscBlue.set_value(self.filtre.get_blue())
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.set_red(self.filtre_init.get_red())
        self.filtre.set_green(self.filtre_init.get_green())
        self.filtre.set_blue(self.filtre_init.get_blue())
        self.init_window()
        
    def on_hscRed_value_changed(self, widget):
        self.filtre.set_red(self.hscRed.get_value())
        
    def on_hscGreen_value_changed(self, widget):
        self.filtre.set_green(self.hscGreen.get_value())

    def on_hscBlue_value_changed(self, widget):
        self.filtre.set_blue(self.hscBlue.get_value())
