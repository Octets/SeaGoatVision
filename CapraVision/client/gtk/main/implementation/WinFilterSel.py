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

from CapraVision.client.gtk import get_ui 
from CapraVision.client.gtk import win_name

from CapraVision.server import filters

from gi.repository import Gtk

class WinFilterSel:
    """Allow the user to select a filter to add to the filterchain"""
    
    def __init__(self):
        self.filter_list = filters.load_filters()
        ui = get_ui(self, 'filtersListStore')
        self.window = ui.get_object(win_name(self))
        self.filtersListStore = ui.get_object('filtersListStore')
        self.lstFilters = ui.get_object('lstFilters')

        self.window.set_modal(True)
        for name, filtre in self.filter_list.items():
            self.filtersListStore.append([name, filtre.__doc__])
        self.filtersListStore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        
        self.selected_filter = None
        
    def get_selected_filter(self):
        _, iterator = self.lstFilters.get_selection().get_selected()
        filter_name = self.filtersListStore.get_value(iterator, 0)
        return self.filter_list[filter_name]
    
    def on_btnOK_clicked(self, widget):
        self.selected_filter = self.get_selected_filter()
        self.window.destroy()
    
    def on_btnCancel_clicked(self, widget):
        self.window.destroy()
    
    def on_lstFilters_button_press_event(self, widget, event):
        if event.get_click_count()[1] == 2L:
            self.selected_filter = self.get_selected_filter()
            self.window.response(Gtk.ResponseType.OK)
            self.window.destroy()
