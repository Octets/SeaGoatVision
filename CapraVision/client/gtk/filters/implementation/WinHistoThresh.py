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

class WinHistoThresh:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.chkChannel1 = ui.get_object('chkChannel1')
        self.spnChannel1Min = ui.get_object('spnChannel1Min')
        self.spnChannel1Min.set_adjustment(self.create_adj())
        self.spnChannel1Max = ui.get_object('spnChannel1Max')
        self.spnChannel1Max.set_adjustment(self.create_adj())
        self.spnChannel1Size = ui.get_object('spnChannel1Size')
        self.spnChannel1Size.set_adjustment(self.create_adj())        
        self.chkChannel2 = ui.get_object('chkChannel2')
        self.spnChannel2Min = ui.get_object('spnChannel2Min')
        self.spnChannel2Min.set_adjustment(self.create_adj())
        self.spnChannel2Max = ui.get_object('spnChannel2Max')
        self.spnChannel2Max.set_adjustment(self.create_adj())
        self.spnChannel2Size = ui.get_object('spnChannel2Size')
        self.spnChannel2Size.set_adjustment(self.create_adj())
        self.chkChannel3 = ui.get_object('chkChannel3')
        self.spnChannel3Min = ui.get_object('spnChannel3Min')
        self.spnChannel3Min.set_adjustment(self.create_adj())
        self.spnChannel3Max = ui.get_object('spnChannel3Max')
        self.spnChannel3Max.set_adjustment(self.create_adj())
        self.spnChannel3Size = ui.get_object('spnChannel3Size')
        self.spnChannel3Size.set_adjustment(self.create_adj())
        self.spnThreshold = ui.get_object('spnThreshold')
        self.spnThreshold.set_adjustment(self.create_adj())
        self.spnMaxValue = ui.get_object('spnMaxValue')
        self.spnMaxValue.set_adjustment(self.create_adj())
        
        self.init_window()
        
    def init_window(self):
        self.chkChannel1.set_active(
                            self.filtre_init.channel1.get_current_value() == 1)
        self.spnChannel1Min.set_value(
                            self.filtre_init.channel1_min.get_current_value())
        self.spnChannel1Max.set_value(
                            self.filtre_init.channel1_max.get_current_value())
        self.spnChannel1Size.set_value(
                            self.filtre_init.channel1_size.get_current_value())
        self.chkChannel2.set_active(
                            self.filtre_init.channel2.get_current_value() == 1)
        self.spnChannel2Min.set_value(
                            self.filtre_init.channel2_min.get_current_value())
        self.spnChannel2Max.set_value(
                            self.filtre_init.channel2_max.get_current_value())
        self.spnChannel2Size.set_value(
                            self.filtre_init.channel2_size.get_current_value())
        self.chkChannel3.set_active(
                            self.filtre_init.channel3.get_current_value() == 1)
        self.spnChannel3Min.set_value(
                            self.filtre_init.channel3_min.get_current_value())
        self.spnChannel3Max.set_value(
                            self.filtre_init.channel3_max.get_current_value())
        self.spnChannel3Size.set_value(
                            self.filtre_init.channel3_size.get_current_value())
        self.spnThreshold.set_value(
                            self.filtre_init.threshold.get_current_value())
        self.spnMaxValue.set_value(
                            self.filtre_init.max_value.get_current_value())
        
    def create_adj(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)

    def on_btnCancel_clicked(self, widget):
        self.filtre.channel1.set_current_value(
                                self.filtre_init.channel1.get_current_value())
        self.filtre.channel1_min.set_current_value(
                            self.filtre_init.channel1_min.get_current_value())
        self.filtre.channel1_max.set_current_value(
                            self.filtre_init.channel1_max.get_current_value())
        self.filtre.channel1_size.set_current_value(
                            self.filtre_init.channel1_size.get_current_value())
        self.filtre.channel2.set_current_value(
                                self.filtre_init.channel2.get_current_value())
        self.filtre.channel2_min.set_current_value(
                            self.filtre_init.channel2_min.get_current_value())
        self.filtre.channel2_max.set_current_value(
                            self.filtre_init.channel2_max.get_current_value())
        self.filtre.channel2_size.set_current_value(
                            self.filtre_init.channel2_size.get_current_value())
        self.filtre.channel3.set_current_value(
                                self.filtre_init.channel3.get_current_value())
        self.filtre.channel3_min.set_current_value(
                            self.filtre_init.channel3_min.get_current_value())
        self.filtre.channel3_max.set_current_value(
                            self.filtre_init.channel3_max.get_current_value())
        self.filtre.channel3_size.set_current_value(
                            self.filtre_init.channel3_size.get_current_value())
        self.filtre.threshold.set_current_value(
                            self.filtre_init.threshold.get_current_value())
        self.filtre.max_value.set_current_value(
                            self.filtre_init.max_value.get_current_value())
        
        self.init_window()
    
    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()
    
    def on_chkChannel1_toggled(self, widget):
        if self.chkChannel1.get_active():
            self.filtre.channel1.set_current_value(1)
        else:
            self.filtre.channel1.set_current_value(0)

    def on_spnChannel1Min_value_changed(self, widget):
        self.filtre.channel1_min.set_current_value(
                                            self.spnChannel1Min.get_value())

    def on_spnChannel1Max_value_changed(self, widget):
        self.filtre.channel1_max.set_current_value(
                                            self.spnChannel1Max.get_value())

    def on_spnChannel1Size_value_changed(self, widget):
        self.filtre.channel1_size.set_current_value(
                                            self.spnChannel1Size.get_value())
    
    def on_chkChannel2_toggled(self, widget):
        if self.chkChannel2.get_active():
            self.filtre.channel2.set_current_value(1)
        else:
            self.filtre.channel2.set_current_value(0)

    def on_spnChannel2Min_value_changed(self, widget):
        self.filtre.channel2_min.set_current_value(
                                            self.spnChannel2Min.get_value())

    def on_spnChannel2Max_value_changed(self, widget):
        self.filtre.channel2_max.set_current_value(
                                            self.spnChannel2Max.get_value())

    def on_spnChannel2Size_value_changed(self, widget):
        self.filtre.channel2_size.set_current_value(
                                            self.spnChannel2Size.get_value())

    def on_chkChannel3_toggled(self, widget):
        if self.chkChannel3.get_active():
            self.filtre.channel3.set_current_value(1)
        else:
            self.filtre.channel3.set_current_value(0)
    
    def on_spnChannel3Min_value_changed(self, widget):
        self.filtre.channel3_min.set_current_value(
                                            self.spnChannel3Min.get_value())

    def on_spnChannel3Max_value_changed(self, widget):
        self.filtre.channel3_max.set_current_value(
                                            self.spnChannel3Max.get_value())

    def on_spnChannel3Size_value_changed(self, widget):
        self.filtre.channel3_size.set_current_value(
                                            self.spnChannel3Size.get_value())

    def on_spnThreshold_value_changed(self, widget):
        self.filtre.threshold.set_current_value(
                                            self.spnThreshold.get_value())
    
    def on_spnMaxValue_value_changed(self, widget):
        self.filtre.max_value.set_current_value(
                                            self.spnMaxValue.get_value())
        