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

class WinPerspectiveByAngle:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnRotationX = ui.get_object('spnRotationX')
        self.spnRotationX.set_adjustment(self.create_adj_rotation())
        self.spnRotationY = ui.get_object('spnRotationY')
        self.spnRotationY.set_adjustment(self.create_adj_rotation())
        self.spnZoom = ui.get_object('spnZoom')
        self.spnZoom.set_adjustment(self.create_adj_zoom())
        
        self.init_window()

    def init_window(self):
        self.spnRotationX.set_value(
                self.filtre_init.rotationX_.get_current_value())
        self.spnRotationY.set_value(
                self.filtre_init.rotationY_.get_current_value())
        self.spnZoom.set_value(
                self.filtre_init.zoom_.get_current_value())
        
    def create_adj_rotation(self):
        return Gtk.Adjustment(1, -360, 360, 1, 1, 0)

    def create_adj_zoom(self):
        return Gtk.Adjustment(1, 0, 1000, 1, 1, 0)

    def on_btnCancel_clicked(self, widget):
        self.init_window()
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()

    def on_spnRotationX_value_changed(self, widget):
        self.filtre.rotationX_.set_current_value(
                    int(self.spnRotationX.get_value()))    
        self.filtre.configure()
        
    def on_spnRotationY_value_changed(self, widget):
        self.filtre.rotationY_.set_current_value(
                    int(self.spnRotationY.get_value()))    
        self.filtre.configure()
        
    def on_spnZoom_value_changed(self, widget):
        self.filtre.zoom_.set_current_value(
                    int(self.spnZoom.get_value()))    
        self.filtre.configure()
        
