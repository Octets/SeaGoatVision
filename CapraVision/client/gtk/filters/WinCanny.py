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

from CapraVision.client.gtk.utils import get_ui
from CapraVision.client.gtk.utils import win_name

class WinCanny:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnThreshold1 = ui.get_object('spnThreshold1')
        self.spnThreshold1.set_adjustment(self.create_adj())
        self.spnThreshold2 = ui.get_object('spnThreshold2')
        self.spnThreshold2.set_adjustment(self.create_adj())
        self.init_window()
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 65535, 1, 10, 0)

    def init_window(self):
        self.spnThreshold1.set_value(self.filtre_init.threshold1)
        self.spnThreshold2.set_value(self.filtre_init.threshold2)
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.threshold1 = self.filtre_init.threshold1
        self.filtre.threshold2 = self.filtre_init.threshold2
    
    def on_spnThreshold1_value_changed(self, widget):
        self.filtre.threshold1 = self.spnThreshold1.get_value()
    
    def on_spnThreshold2_value_changed(self, widget):
        self.filtre.threshold2 = self.spnThreshold2.get_value()
    
    