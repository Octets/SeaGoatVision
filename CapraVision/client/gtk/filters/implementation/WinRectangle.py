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

from gi.repository import Gtk

from CapraVision.client.gtk import get_ui
from CapraVision.client.gtk import win_name

class WinRectangle:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnX1 = ui.get_object('spnX1')
        self.spnX1.set_adjustment(self.create_adj())
        self.spnX2 = ui.get_object('spnX2')
        self.spnX2.set_adjustment(self.create_adj())
        self.spnY1 = ui.get_object('spnY1')
        self.spnY1.set_adjustment(self.create_adj())
        self.spnY2 = ui.get_object('spnY2')
        self.spnY2.set_adjustment(self.create_adj())
        
        self.init_window()
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 65535, 1, 10, 0)

    def init_window(self):
        self.spnX1.set_value(self.filtre_init.x1.get_current_value())
        self.spnX2.set_value(self.filtre_init.x2.get_current_value())
        self.spnY1.set_value(self.filtre_init.y1.get_current_value())
        self.spnY2.set_value(self.filtre_init.y2.get_current_value())

    def on_spnX1_value_changed(self, widget):
        self.filtre.x1.set_current_value(int(self.spnX1.get_value()))

    def on_spnX2_value_changed(self, widget):
        self.filtre.x2.set_current_value(int(self.spnX2.get_value()))

    def on_spnY1_value_changed(self, widget):
        self.filtre.y1.set_current_value(int(self.spnY1.get_value()))

    def on_spnY2_value_changed(self, widget):
        self.filtre.y2.set_current_value(int(self.spnY2.get_value()))

    def on_btnCancel_clicked(self, widget):
        self.filtre.x1.set_current_value(self.filtre_init.x1.get_current_value())
        self.filtre.x2.set_current_value(self.filtre_init.x2.get_current_value())
        self.filtre.y1.set_current_value(self.filtre_init.y1.get_current_value())
        self.filtre.y2.set_current_value(self.filtre_init.y2.get_current_value())
        self.init_window()
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    