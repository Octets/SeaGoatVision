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

class WinMorphology():

    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnKernelWidth = ui.get_object('spnKernelWidth')
        self.spnKernelWidth.set_adjustment(self.create_adj())
        self.spnKernelHeight = ui.get_object('spnKernelHeight')
        self.spnKernelHeight.set_adjustment(self.create_adj())
        self.spnAnchorX = ui.get_object('spnAnchorX')
        self.spnAnchorX.set_adjustment(self.create_adj_anchor())
        self.spnAnchorY = ui.get_object('spnAnchorY')
        self.spnAnchorY.set_adjustment(self.create_adj_anchor())
        self.spnIterations = ui.get_object('spnIterations')
        self.spnIterations.set_adjustment(self.create_adj())
        self.init_window()
        
    def init_window(self):
        self.spnKernelWidth.set_value(self.filtre_init.get_kernel_width())
        self.spnKernelHeight.set_value(self.filtre_init.get_kernel_height())
        self.spnAnchorX.set_value(self.filtre_init.get_anchor_x())
        self.spnAnchorY.set_value(self.filtre_init.get_anchor_y())
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)

    def create_adj_anchor(self):
        return Gtk.Adjustment(1, -1, 255, 1, 10, 0)
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.set_kernel_width(self.filtre_init.get_kernel_width())
        self.filtre.set_kernel_height(self.filtre_init.get_kernel_height())
        self.filtre.set_anchor_x(self.filtre_init.get_anchor_x())
        self.filtre.set_anchor_y(self.filtre_init.get_anchor_y())
        self.filtre.set_iterations(self.filtre_init.get_iterations())
        self.filtre.configure()
        self.init_window()
    
    def on_spnKernelWidth_value_changed(self, widget):
        self.filtre.set_kernel_width(self.spnKernelWidth.get_value())
        self.filtre.configure()
    
    def on_spnKernelHeight_value_changed(self, widget):
        self.filtre.set_kernel_height(self.spnKernelHeight.get_value())
        self.filtre.configure()
    
    def on_spnAnchorX_value_changed(self, widget):
        self.filtre.set_anchor_x(self.spnAnchorX.get_value())
        self.filtre.configure()
    
    def on_spnAnchorY_value_changed(self, widget):
        self.filtre.set_anchor_y(self.spnAnchorY.get_value())
        self.filtre.configure()
        
    def on_spnIterations_value_changed(self, widget):
        self.filtre.set_iterations(self.spnIterations.get_value())
        self.filtre.configure()
    