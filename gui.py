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

'''
Created on 2012-07-23

@author: Benoit Paquet
'''

import pygtk
pygtk.require("2.0")
import gtk
import chain

def get_ui(window, *names):
    ui = gtk.Builder()
    ui.add_objects_from_file('gui.glade', [name for name in names])
    ui.connect_signals(window)
    return ui

class WinFilterChain:
    
    def __init__(self):
        ui = get_ui(self, 'winFilterChain', 'filtersListStore', 'sourcesListStore')
        self.window = ui.get_object('winFilterChain')
        self.chain = chain.FilterChain()
    
    def init_window(self):
        pass
    
    def on_btnOpen_clicked(self, widget):
        pass
    
    def on_btnSource_clicked(self, widget):
        pass
    
    def on_btnAdd_clicked(self, widget):
        pass
    
    def on_btnRemove_clicked(self, widget):
        pass
    
    def on_btnConfig_clicked(self, widget):
        pass
    
    def on_btnView_clicked(self, widget):
        pass
    
    def on_btnCreate_clicked(self, widget):
        pass
    
    def on_btnSave_clicked(self, widget):
        pass

    def on_btnSaveAs_clicked(self, widget):
        pass
    
    def on_btnCancel_clicked(self, widget):
        pass
    
    def on_btnQuit_clicked(self, widget):
        pass
    
    def on_cboSource_changed(self, widget):
        pass
    