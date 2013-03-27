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

class WinMTI880:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.spnHueMin = ui.get_object('spnHueMin')
        self.spnHueMin.set_adjustment(self.create_adj_hue())
        self.spnHueMax = ui.get_object('spnHueMax')
        self.spnHueMax.set_adjustment(self.create_adj_hue())
        self.spnAreaMin = ui.get_object('spnAreaMin')
        self.spnAreaMin.set_adjustment(self.create_adj())
        self.spnNormal = ui.get_object('spnNormalHand')
        self.spnNormal.set_adjustment(self.create_adj())
        self.spnExtended = ui.get_object('spnExtendedHand')
        self.spnExtended.set_adjustment(self.create_adj())
        self.spnClosed = ui.get_object('spnClosedHand')
        self.spnClosed.set_adjustment(self.create_adj())
        self.spnAmplitude = ui.get_object('spnAmplitude')
        self.spnAmplitude.set_adjustment(self.create_adj())
        self.lblHue = ui.get_object('lblHue')
        self.lblNormal = ui.get_object('lblNormal')
        self.lblExtended = ui.get_object('lblExtended')
        self.lblClosed = ui.get_object('lblClosed')
        
        self.filtre.add_observer(self.filter_observer)
        
        self.init_window()
        
    def create_adj_hue(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)

    def create_adj(self):
        return Gtk.Adjustment(1, 1, 999999, 1, 10, 0)

    def init_window(self):
        self.spnAreaMin.set_value(self.filtre_init.area_min)
        self.spnClosed.set_value(self.filtre_init.closed_hand)
        self.spnNormal.set_value(self.filtre_init.normal_hand)
        self.spnExtended.set_value(self.filtre_init.extended_hand)
        self.spnHueMax.set_value(self.filtre_init.hue_max)
        self.spnHueMin.set_value(self.filtre_init.hue_min)
        self.spnAmplitude.set_value(self.filtre_init.amplitude)
        
    def filter_observer(self):
        self.spnClosed.set_value(self.filtre.closed_hand)
        self.spnNormal.set_value(self.filtre.normal_hand)
        self.spnExtended.set_value(self.filtre.extended_hand)
        self.spnHueMax.set_value(self.filtre.hue_max)
        self.spnHueMin.set_value(self.filtre.hue_min)
        
        if not self.filtre._capture_closed_hand:
            self.lblClosed.set_text('')
        if not self.filtre._capture_extended_hand:
            self.lblExtended.set_text('')
        if not self.filtre._capture_normal_hand:
            self.lblNormal.set_text('')
        if not self.filtre._calibrate_hue:
            self.lblHue.set_text('')

    def on_btnOK_clicked(self, widget):
        self.filtre.remove_observer(self.init_window)
        self.cb()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.filtre.area_min = self.filtre_init.area_min
        self.filtre.closed_hand = self.filtre_init.closed_hand
        self.filtre.normal_hand = self.filtre_init.normal_hand
        self.filtre.extended_hand = self.filtre_init.extended_hand
        self.filtre.hue_max = self.filtre_init.hue_max
        self.filtre.hue_min = self.filtre_init.hue_min
        self.filtre.amplitude = self.filtre_init.amplitude
        self.init_window()
    
    def on_btnHue_clicked(self, widget):
        self.filtre.hue_min = 0
        self.filtre._calibrate_hue = True
        self.lblHue.set_text('Calibrating')
        
    def on_btnNormal_clicked(self, widget):
        self.filtre._capture_normal_hand = True
        self.lblNormal.set_text('Calibrating')
        
    def on_btnClosed_clicked(self, widget):
        self.filtre._capture_closed_hand = True
        self.lblClosed.set_text('Calibrating')
        
    def on_btnExtended_clicked(self, widget):
        self.filtre._capture_extended_hand = True
        self.lblExtended.set_text('Calibrating')
        
    def on_spnAreaMin_value_changed(self, widget):
        self.filtre.area_min = int(self.spnAreaMin.get_value())
    
    def on_spnClosedHand_value_changed(self, widget):
        if not self.filtre._capture_closed_hand:
            self.filtre.closed_hand = int(self.spnClosed.get_value())
    
    def on_spnNormalHand_value_changed(self, widget):
        if not self.filtre._capture_normal_hand:
            self.filtre.normal_hand = int(self.spnNormal.get_value())
    
    def on_spnExtendedHand_value_changed(self, widget):
        if not self.filtre._capture_extended_hand:
            self.filtre.extended_hand =  int(self.spnExtended.get_value())
    
    def on_spnHueMin_value_changed(self, widget):
        if not self.filtre._calibrate_hue:
            self.filtre.hue_min = int(self.spnHueMin.get_value())
    
    def on_spnHueMax_value_changed(self, widget):
        if not self.filtre._calibrate_hue:
            self.filtre.hue_max = int(self.spnHueMax.get_value())
        
    def on_spnAmplitude_value_changed(self, widget):
        self.filtre.amplitude = self.spnAmplitude.get_value()
        
    