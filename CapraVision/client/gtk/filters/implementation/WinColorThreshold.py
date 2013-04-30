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

class WinColorThreshold:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.hscc1min = ui.get_object('hscc1min')
        self.hscc1max = ui.get_object('hscc1max')
        self.hscc2min = ui.get_object('hscc2min')
        self.hscc2max = ui.get_object('hscc2max')
        self.hscc3min = ui.get_object('hscc3min')
        self.hscc3max = ui.get_object('hscc3max')
        self.init_window()
        
    def init_window(self):
        self.hscc1min.set_range(0, 255)
        self.hscc1min.set_value(self.filtre.c1min.get_current_value())
        self.hscc1max.set_range(0, 255)
        self.hscc1max.set_value(self.filtre.c1max.get_current_value())
        self.hscc2min.set_range(0, 255)
        self.hscc2min.set_value(self.filtre.c2min.get_current_value())
        self.hscc2max.set_range(0, 255)
        self.hscc2max.set_value(self.filtre.c2max.get_current_value())
        self.hscc3min.set_range(0, 255)
        self.hscc3min.set_value(self.filtre.c3min.get_current_value())
        self.hscc3max.set_range(0, 255)
        self.hscc3max.set_value(self.filtre.c3max.get_current_value())
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
        
    def on_btnCancel_clicked(self, widget):
        self.filtre.c1min = self.filtre_init.c1min
        self.filtre.c1max = self.filtre_init.c1max
        self.filtre.c2min = self.filtre_init.c2min
        self.filtre.c2max = self.filtre_init.c2max
        self.filtre.c3min = self.filtre_init.c3min
        self.filtre.c3max = self.filtre_init.c3max
        
        self.init_window()
        
    def on_hscc1min_value_changed(self, widget):
        self.filtre.c1min.set_current_value(self.hscc1min.get_value())
        self.filtre.configure()
        
    def on_hscc1max_value_changed(self, widget):
        self.filtre.c1max.set_current_value(self.hscc1max.get_value())
        self.filtre.configure()
        
    def on_hscc2min_value_changed(self, widget):
        self.filtre.c2min.set_current_value(self.hscc2min.get_value())
        self.filtre.configure()

    def on_hscc2max_value_changed(self, widget):
        self.filtre.c2max.set_current_value(self.hscc2max.get_value())
        self.filtre.configure()

    def on_hscc3min_value_changed(self, widget):
        self.filtre.c3min.set_current_value(self.hscc3min.get_value())
        self.filtre.configure()

    def on_hscc3max_value_changed(self, widget):
        self.filtre.c3max.set_current_value(self.hscc3max.get_value())
        self.filtre.configure()
