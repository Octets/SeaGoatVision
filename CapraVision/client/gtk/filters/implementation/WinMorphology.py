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
        self.spnKernelWidth.set_value(self.filtre_init.kernel_width.get_current_value())
        self.spnKernelHeight.set_value(self.filtre_init.kernel_height.get_current_value())
        self.spnAnchorX.set_value(self.filtre_init.anchor_x.get_current_value())
        self.spnAnchorY.set_value(self.filtre_init.anchor_y.get_current_value())
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)

    def create_adj_anchor(self):
        return Gtk.Adjustment(1, -1, 255, 1, 10, 0)
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.kernel_width = self.filtre_init.kernel_width
        self.filtre.kernel_height = self.filtre_init.kernel_height
        self.filtre.anchor_x = self.filtre_init.anchor_x
        self.filtre.anchor_y = self.filtre_init.anchor_y
        self.filtre.iterations = self.filtre_init.iterations
        self.filtre.configure()
        self.init_window()
    
    def on_spnKernelWidth_value_changed(self, widget):
        self.filtre.kernel_width.set_current_value(self.spnKernelWidth.get_value())
        self.filtre.configure()
    
    def on_spnKernelHeight_value_changed(self, widget):
        self.filtre.kernel_height.set_current_value(self.spnKernelHeight.get_value())
        self.filtre.configure()
    
    def on_spnAnchorX_value_changed(self, widget):
        self.filtre.anchor_x.set_current_value(self.spnAnchorX.get_value())
        self.filtre.configure()
    
    def on_spnAnchorY_value_changed(self, widget):
        self.filtre.anchor_y.set_current_value(self.spnAnchorY.get_value())
        self.filtre.configure()
        
    def on_spnIterations_value_changed(self, widget):
        self.filtre.iterations.set_current_value(self.spnIterations.get_value())
        self.filtre.configure()
    