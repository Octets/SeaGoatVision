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

class WinGaussianBlur:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnHeight = ui.get_object('spnHeight')
        self.spnHeight.set_adjustment(self.create_adj_kernel())
        self.spnWidth = ui.get_object('spnWidth')
        self.spnWidth.set_adjustment(self.create_adj_kernel())
        self.spnX = ui.get_object('spnX')
        self.spnX.set_adjustment(self.create_adj_sigma())
        self.spnY = ui.get_object('spnY')
        self.spnY.set_adjustment(self.create_adj_sigma())
    
    def create_adj_kernel(self):
        return Gtk.Adjustment(1, 1, 65535, 2, 10, 0)
    
    def create_adj_sigma(self):
        return Gtk.Adjustment(1, 1, 65535, 1, 10, 0)
    
    def init_window(self):
        self.spnHeight.set_value(self.filtre_init.kernel_height)
        self.spnWidth.set_value(self.filtre_init.kernel_width)
        self.spnX.set_value(self.filtre_init.sigma_x)
        self.spnY.set_value(self.filtre_init.sigma_y)
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.kernel_height = self.filtre_init.kernel_height
        self.filtre.kernel_width = self.filtre_init.kernel_width
        self.filtre.sigma_x = self.filtre_init.sigma_x
        self.filtre.sigma_y = self.filtre_init.sigma_y
        self.init_window()
    
    def on_spnHeight_value_changed(self, widget):
        self.filtre.kernel_height = int(self.spnHeight.get_value())
    
    def on_spnWidth_value_changed(self, widget):
        self.filtre.kernel_width = int(self.spnWidth.get_value())
    
    def on_spnX_value_changed(self, widget):
        self.filtre.sigma_x = int(self.spnX.get_value())
    
    def on_spnY_value_changed(self, widget):
        self.filtre.sigma_y = int(self.spnY.get_value())
    