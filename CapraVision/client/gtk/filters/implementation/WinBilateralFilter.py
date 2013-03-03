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

class WinBilateralFilter():

    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnDiameter = ui.get_object('spnDiameter')
        self.spnDiameter.set_adjustment(self.create_adj())
        self.spnSigmaColor = ui.get_object('spnSigmaColor')
        self.spnSigmaColor.set_adjustment(self.create_adj())
        self.spnSigmaSpace = ui.get_object('spnSigmaSpace')
        self.spnSigmaSpace.set_adjustment(self.create_adj())
        self.init_window()
        
    def init_window(self):
        self.spnDiameter.set_value(self.filtre_init.diameter.get_current_value())
        self.spnSigmaColor.set_value(self.filtre_init.sigma_color.get_current_value())
        self.spnSigmaSpace.set_value(self.filtre_init.sigma_space.get_current_value())
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)
        
    def on_btnCancel_clicked(self, widget):
        self.filtre.diameter = self.filtre_init.diameter
        self.filtre.sigma_color = self.filtre_init.sigma_color
        self.filtre.sigma_space = self.filtre_init.sigma_space
        self.init_window()
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()

    def on_spnDiameter_value_changed(self, widget):
        self.filtre.diameter.set_current_value(self.spnDiameter.get_value())
        
    def on_spnSigmaColor_value_changed(self, widget):
        self.filtre.sigma_color.set_current_value(self.spnSigmaColor.get_value())

    def on_spnSigmaSpace_value_changed(self, widget):
        self.filtre.sigma_space.set_current_value(self.spnSigmaSpace.get_value())
