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

class WinColorThreshold:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.hscRedMin = ui.get_object('hscRedMin')
        self.hscRedMax = ui.get_object('hscRedMax')
        self.hscBlueMin = ui.get_object('hscBlueMin')
        self.hscBlueMax = ui.get_object('hscBlueMax')
        self.hscGreenMin = ui.get_object('hscGreenMin')
        self.hscGreenMax = ui.get_object('hscGreenMax')
        self.init_window()
        
    def init_window(self):
        self.hscRedMin.set_range(0, 255)
        self.hscRedMin.set_value(self.filtre.redmin)
        self.hscRedMax.set_range(0, 255)
        self.hscRedMax.set_value(self.filtre.redmax)
        self.hscGreenMin.set_range(0, 255)
        self.hscGreenMin.set_value(self.filtre.greenmin)
        self.hscGreenMax.set_range(0, 255)
        self.hscGreenMax.set_value(self.filtre.greenmax)
        self.hscBlueMin.set_range(0, 255)
        self.hscBlueMin.set_value(self.filtre.bluemin)
        self.hscBlueMax.set_range(0, 255)
        self.hscBlueMax.set_value(self.filtre.bluemax)
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
        
    def on_btnCancel_clicked(self, widget):
        self.filtre.redmin = self.filtre_init.redmin
        self.filtre.redmax = self.filtre_init.redmax
        self.filtre.greenmin = self.filtre_init.greenmin
        self.filtre.greenmax = self.filtre_init.greenmax
        self.filtre.bluemin = self.filtre_init.bluemin
        self.filtre.bluemax = self.filtre_init.bluemax
        
        self.init_window()
        
    def on_hscRedMin_value_changed(self, widget):
        self.filtre.redmin = self.hscRedMin.get_value()
        self.filtre.configure()
        
    def on_hscRedMax_value_changed(self, widget):
        self.filtre.redmax = self.hscRedMax.get_value()
        self.filtre.configure()
        
    def on_hscGreenMin_value_changed(self, widget):
        self.filtre.greenmin = self.hscGreenMin.get_value()
        self.filtre.configure()

    def on_hscGreenMax_value_changed(self, widget):
        self.filtre.greenmax = self.hscGreenMax.get_value()
        self.filtre.configure()

    def on_hscBlueMin_value_changed(self, widget):
        self.filtre.bluemin = self.hscBlueMin.get_value()
        self.filtre.configure()

    def on_hscBlueMax_value_changed(self, widget):
        self.filtre.bluemax = self.hscBlueMax.get_value()
        self.filtre.configure()
