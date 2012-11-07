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
from CapraVision.client.gtk.utils import *

class WinPerspective:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self, 'adjPerspective')
        self.window = ui.get_object(win_name(self))
        self.spnTopLeftX = ui.get_object('spnTopLeftX')
        self.spnTopLeftY = ui.get_object('spnTopLeftY')
        self.spnBottomLeftX = ui.get_object('spnBottomLeftX')
        self.spnBottomLeftY = ui.get_object('spnBottomLeftY')
        self.spnTopRightX = ui.get_object('spnTopRightX')
        self.spnTopRightY = ui.get_object('spnTopRightY')
        self.spnBottomRightX = ui.get_object('spnBottomRightX')
        self.spnBottomRightY = ui.get_object('spnBottomRightY')
        self.init_window()
        
    def init_window(self):
        self.spnTopLeftX.set_adjustment(self.create_adj())
        self.spnTopLeftX.set_value(self.filtre.topleftx)
        self.spnTopLeftY.set_adjustment(self.create_adj())
        self.spnTopLeftY.set_value(self.filtre.toplefty)
        self.spnBottomLeftX.set_adjustment(self.create_adj())
        self.spnBottomLeftX.set_value(self.filtre.bottomleftx)
        self.spnBottomLeftY.set_adjustment(self.create_adj())
        self.spnBottomLeftY.set_value(self.filtre.bottomlefty)
        self.spnTopRightX.set_adjustment(self.create_adj())
        self.spnTopRightX.set_value(self.filtre.toprightx)
        self.spnTopRightY.set_adjustment(self.create_adj())
        self.spnTopRightY.set_value(self.filtre.toprighty)
        self.spnBottomRightX.set_adjustment(self.create_adj())
        self.spnBottomRightX.set_value(self.filtre.bottomrightx)
        self.spnBottomRightY.set_adjustment(self.create_adj())
        self.spnBottomRightY.set_value(self.filtre.bottomrighty)
        
    def create_adj(self):
        return Gtk.Adjustment(0.0, 0.0, 65535.0, 1, 10.0, 0.0)
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
        
    def on_btnCancel_clicked(self, widget):
        self.filtre.topleftx = self.filtre_init.topleftx
        self.filtre.toplefty = self.filtre_init.toplefty
        self.filtre.bottomleftx = self.filtre_init.bottomleftx
        self.filtre.bottomlefty = self.filtre_init.bottomlefty
        self.filtre.toprightx = self.filtre_init.toprightx
        self.filtre.toprighty = self.filtre_init.toprighty
        self.filtre.bottomrightx = self.filtre_init.bottomrightx
        self.filtre.bottomrighty = self.filtre_init.bottomrighty
        self.init_window()
        
    def on_spnTopLeftX_value_changed(self, widget):
        self.filtre.topleftx = self.spnTopLeftX.get_value()
        self.filtre.configure()
        
    def on_spnTopLeftY_value_changed(self, widget):
        self.filtre.toplefty = self.spnTopLeftY.get_value()
        self.filtre.configure()

    def on_spnBottomLeftX_value_changed(self, widget):
        self.filtre.bottomleftx = self.spnBottomLeftX.get_value()
        self.filtre.configure()
        
    def on_spnBottomLeftY_value_changed(self, widget):
        self.filtre.bottomlefty = self.spnBottomLeftY.get_value()
        self.filtre.configure()
        
    def on_spnTopRightX_value_changed(self, widget):
        self.filtre.toprightx = self.spnTopRightX.get_value()
        self.filtre.configure()

    def on_spnTopRightY_value_changed(self, widget):
        self.filtre.toprighty = self.spnTopRightY.get_value()
        self.filtre.configure()
        
    def on_spnBottomRightX_value_changed(self, widget):
        self.filtre.bottomrightx = self.spnBottomRightX.get_value()
        self.filtre.configure()

    def on_spnBottomRightY_value_changed(self, widget):
        self.filtre.bottomrighty = self.spnBottomRightY.get_value()
        self.filtre.configure()
