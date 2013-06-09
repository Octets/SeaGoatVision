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

class WinSectionFilterCPP:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnKernelErodeHeight = ui.get_object('spnKernelErodeHeight')
        self.spnKernelErodeHeight.set_adjustment(self.create_adj())
        self.spnKernelErodeWidth = ui.get_object('spnKernelErodeWidth')
        self.spnKernelErodeWidth.set_adjustment(self.create_adj())
        self.spnKernelDilateHeight = ui.get_object('spnKernelDilateHeight')
        self.spnKernelDilateHeight.set_adjustment(self.create_adj())
        self.spnKernelDilateWidth = ui.get_object('spnKernelDilateWidth')
        self.spnKernelDilateWidth.set_adjustment(self.create_adj())
        self.spnSections = ui.get_object('spnSections')
        self.spnSections.set_adjustment(self.create_adj())
        self.spnMinimumArea = ui.get_object('spnMinimumArea')
        self.spnMinimumArea.set_adjustment(Gtk.Adjustment(1, 0, 65535, 1, 1, 0))
        self.spnMinLight = ui.get_object('spnMinLight')
        self.spnMinLight.set_adjustment(self.create_adj())
        self.spnMinGrass = ui.get_object('spnMinGrass')
        self.spnMinGrass.set_adjustment(self.create_adj())
        self.spnMaxGrass = ui.get_object('spnMaxGrass')
        self.spnMaxGrass.set_adjustment(self.create_adj())
        self.init_window()

    def init_window(self):
        self.spnKernelErodeHeight.set_value(
                self.filtre_init.kernel_erode_height.get_current_value())
        self.spnKernelErodeWidth.set_value(
                self.filtre_init.kernel_erode_width.get_current_value())
        self.spnKernelDilateHeight.set_value(
                self.filtre_init.kernel_dilate_height.get_current_value())
        self.spnKernelDilateWidth.set_value(
                self.filtre_init.kernel_dilate_width.get_current_value())
        self.spnSections.set_value(
                self.filtre_init.sections.get_current_value())
        self.spnMinimumArea.set_value(
                self.filtre_init.min_area.get_current_value())
        self.spnMinLight.set_value(
                self.filtre_init.light_min.get_current_value())
        self.spnMinGrass.set_value(
                self.filtre_init.grass_min.get_current_value())
        self.spnMaxGrass.set_value(
                self.filtre_init.grass_max.get_current_value())
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 255, 1, 1, 0)

    def on_btnCancel_clicked(self, widget):
        self.init_window()
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()

    def on_spnKernelErodeHeight_value_changed(self, widget):
        self.filtre.kernel_erode_height.set_current_value(
                    int(self.spnKernelErodeHeight.get_value()))    
        self.filtre.configure()
        
    def on_spnKernelErodeWidth_value_changed(self, widget):
        self.filtre.kernel_erode_width.set_current_value(
                    int(self.spnKernelErodeWidth.get_value()))    
        self.filtre.configure()
        
    def on_spnKernelDilateHeight_value_changed(self, widget):
        self.filtre.kernel_dilate_height.set_current_value(
                    int(self.spnKernelDilateHeight.get_value()))    
        self.filtre.configure()
        
    def on_spnKernelDilateWidth_value_changed(self, widget):
        self.filtre.kernel_dilate_width.set_current_value(
                    int(self.spnKernelDilateWidth.get_value()))    
        self.filtre.configure()
        
    def on_spnSections_value_changed(self, widget):
        self.filtre.sections.set_current_value(
                    int(self.spnSections.get_value()))    
        self.filtre.configure()

    def on_spnMinimumArea_value_changed(self, widget):
        self.filtre.min_area.set_current_value(
                    int(self.spnMinimumArea.get_value()))    
        self.filtre.configure()

    def on_spnMinLight_value_changed(self, widget):
        self.filtre.light_min.set_current_value(
                    int(self.spnMinLight.get_value()))    
        self.filtre.configure()

    def on_spnMinGrass_value_changed(self, widget):
        self.filtre.grass_min.set_current_value(
                    int(self.spnMinGrass.get_value()))    
        self.filtre.configure()

    def on_spnMaxGrass_value_changed(self, widget):
        self.filtre.grass_max.set_current_value(
                    int(self.spnMaxGrass.get_value()))    
        self.filtre.configure()

