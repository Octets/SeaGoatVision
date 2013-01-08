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

from CapraVision.client.qt.utils import *
from CapraVision.server import filters
from PySide import QtGui
from PySide import QtCore

class WinFilterSel(QtCore.QObject):
    """Allow the user to select a filter to add to the filterchain"""
    onAddFilter = QtCore.Signal(object)
    def __init__(self):
        super(WinFilterSel, self).__init__()
        self.ui = get_ui(self)
        self.filters = filters.load_filters()
        
        
        self.ui.addFilterButton.clicked.connect(self._addFilter)
        
        for name, filter in self.filters.items():
            self.ui.filterListWidget.addItem(name)  
        
    def _addFilter(self):
        self.onAddFilter.emit(self.ui.filterListWidget.currentItem().text())
