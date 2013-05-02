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
from gi.repository import GObject

from CapraVision.client.gtk import get_ui
from CapraVision.client.gtk import win_name

class WinMarioBros3FinalWorldView:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnCenterX = ui.get_object('spnCenterX')
        self.spnCenterX.set_adjustment(self.create_adj())
        self.spnCenterY = ui.get_object('spnCenterY')
        self.spnCenterY.set_adjustment(self.create_adj())
        self.spnSizeX = ui.get_object('spnSizeX')
        self.spnSizeX.set_adjustment(self.create_adj())
        self.spnSizeY = ui.get_object('spnSizeY')
        self.spnSizeY.set_adjustment(self.create_adj())
                 
        self.init_window()
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)

    def init_window(self):
        self.spnCenterX.set_value(self.filtre_init.center_x)
        self.spnCenterY.set_value(self.filtre_init.center_y)
        self.spnSizeX.set_value(self.filtre_init.size_x)
        self.spnSizeY.set_value(self.filtre_init.size_y)
                
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.center_x = self.filtre_init.center_x
        self.filtre.center_y = self.filtre_init.center_y
        self.filtre.size_x = self.filtre_init.size_x
        self.filtre.size_y = self.filtre_init.size_y
        
        self.init_window()
            
    def on_spnCenterX_value_changed(self, widget):
        self.filtre.center_x = int(self.spnCenterX.get_value())
        self.filtre.configure()
        
    def on_spnCenterY_value_changed(self, widget):
        self.filtre.center_y = int(self.spnCenterY.get_value())
        self.filtre.configure()
    
    def on_spnSizeX_value_changed(self, widget):
        self.filtre.size_x = int(self.spnSizeX.get_value())
        self.filtre.configure()
    
    def on_spnSizeY_value_changed(self, widget):
        self.filtre.size_y =  int(self.spnSizeY.get_value())
        self.filtre.configure()
            