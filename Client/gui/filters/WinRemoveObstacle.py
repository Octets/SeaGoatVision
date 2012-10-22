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

class WinRemoveObstacle:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnThreshold =ui.get_object('spnThreshold')
        self.spnThreshold.set_adjustment(self.create_adj())
        self.spnVBlur = ui.get_object('spnVBlur')
        self.spnVBlur.set_adjustment(self.create_adj())
        self.spnHBlur = ui.get_object('spnHBlur')
        self.spnHBlur.set_adjustment(self.create_adj())
        
        self.init_window()

    def init_window(self):
        self.spnThreshold.set_value(self.filtre_init.threshold)
        
    def create_adj(self):
        return Gtk.Adjustment(1, 0, 255, 1, 1, 0)

    def on_btnCancel_clicked(self, widget):
        self.init_window()
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_spnThreshold_value_changed(self, widget):
        self.filtre.threshold = self.spnThreshold.get_value()
    
    def on_spnVBlur_value_changed(self, widget):
        self.filtre.vertical_blur = self.sp
        