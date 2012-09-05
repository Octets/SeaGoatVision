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
"""Contains the user interfaces to configure the filters.

To add a new ui, the constructor must receive the filter to configure
and the name must be as follow: WinFilterName
"""

from gi.repository import Gtk
from utils import get_ui, win_name
import copy, sys, inspect

def map_filter_to_ui(filter):
    """Returns the appropriate window class to configure the filter"""
    for win in vars(sys.modules[__name__]).values():
        if inspect.isclass(win):
            if win.__name__ == 'Win' + filter.__class__.__name__:
                return win
    return None

class WinColorLevel:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.hscRed = ui.get_object('hscRed')
        self.hscGreen = ui.get_object('hscGreen')
        self.hscBlue = ui.get_object('hscBlue')
        self.init_window()
        
    def init_window(self):
        self.hscRed.set_range(0, 100)
        self.hscRed.set_value(self.filtre.red)
        self.hscGreen.set_range(0, 100)
        self.hscGreen.set_value(self.filtre.green)
        self.hscBlue.set_range(0, 100)
        self.hscBlue.set_value(self.filtre.blue)
        
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.red = self.filtre_init.red
        self.filtre.green = self.filtre_init.green
        self.filtre.blue = self.filtre_init.blue
        self.init_window()
        
    def on_hscRed_value_changed(self, widget):
        self.filtre.red = self.hscRed.get_value()
        
    def on_hscGreen_value_changed(self, widget):
        self.filtre.green = self.hscGreen.get_value()

    def on_hscBlue_value_changed(self, widget):
        self.filtre.blue = self.hscBlue.get_value()
    
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
        
class WinExec:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.txtCurrent = ui.get_object('txtCurrent')
        self.txtWorking = ui.get_object('txtWorking')
        
        self.init_window()
        
    def init_window(self):
        self.txtCurrent.get_buffer().set_text(self.filtre.code)
        self.txtWorking.get_buffer().set_text(self.filtre.code)
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
        
    def on_btnCancel_clicked(self, widget):
        self.filtre.code = self.filtre_init.code
        self.init_window()

    def on_btnApply_clicked(self, widget):
        start, end = self.txtWorking.get_buffer().get_bounds()
        code = self.txtWorking.get_buffer().get_text(start, end, False)
        self.txtCurrent.get_buffer().set_text(code)
        self.filtre.code = code
    