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

class WinHoughTransform:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnCanny1 = ui.get_object('spnCanny1')
        self.spnCanny1.set_adjustment(self.create_adj())
        self.spnCanny2 = ui.get_object('spnCanny2')
        self.spnCanny2.set_adjustment(self.create_adj())
        self.spnRho = ui.get_object('spnRho')
        self.spnRho.set_adjustment(self.create_adj())
        self.spnTheta = ui.get_object('spnTheta')
        self.spnTheta.set_adjustment(self.create_adj())
        self.spnThreshold = ui.get_object('spnThreshold')
        self.spnThreshold.set_adjustment(self.create_adj())
        self.spnLineSize = ui.get_object('spnLineSize')
        self.spnLineSize.set_adjustment(self.create_adj())
        self.init_window()
        
    def init_window(self):
        self.spnCanny1.set_value(self.filtre_init.canny1)
        self.spnCanny2.set_value(self.filtre_init.canny2)
        self.spnRho.set_value(self.filtre_init.rho)
        self.spnTheta.set_value(self.filtre_init.theta)
        self.spnThreshold.set_value(self.filtre_init.threshold)
        self.spnLineSize.set_value(self.filtre_init.line_size)
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 65535, 1, 10, 0)

    def on_spnCanny1_value_changed(self, widget):
        self.filtre.canny1 = int(self.spnCanny1.get_value())
    
    def on_spnCanny2_value_changed(self, widget):
        self.filtre.canny2 = int(self.spnCanny2.get_value())
    
    def on_spnRho_value_changed(self, widget):
        self.filtre.rho = int(self.spnRho.get_value())
    
    def on_spnTheta_value_changed(self, widget):
        self.filtre.theta = int(self.spnTheta.get_value())
    
    def on_spnThreshold_value_changed(self, widget):
        self.filtre.threshold = int(self.spnThreshold.get_value())
    
    def on_spnLineSize_value_changed(self, widget):
        self.filtre.line_size = int(self.spnLineSize.get_value())
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.canny1 = self.filtre_init.canny1
        self.filtre.canny2 = self.filtre_init.canny2
        self.filtre.rho = self.filtre_init.rho
        self.filtre.theta = self.filtre_init.theta
        self.filtre.threshold = self.filtre_init.threshold
        self.filtre.line_size = self.filtre_init.line_size
        self.init_window()
    