#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
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

from SeaGoatVision.client.qt.utils import get_ui
from PySide import QtCore

class WinFilterList(QtCore.QObject):
    """Allow the user to select a filter to add to the filterchain"""
    onAddFilter = QtCore.Signal(object)
    def __init__(self, controller):
        super(WinFilterList, self).__init__()
        self.ui = get_ui(self)
        self.controller = controller

        self.ui.addFilterButton.clicked.connect(self._addFilter)
        self.ui.reloadFilterButton.clicked.connect(self._reloadFilter)
        self.ui.filterListWidget.doubleClicked.connect(self._addFilter)

        self.reload_list_filter(self.controller.get_filter_list())

    def reload_list_filter(self, lst_filter):
        lst_filter_sort = lst_filter[:]
        lst_filter_sort.sort()
        for name in lst_filter_sort:
            self.ui.filterListWidget.addItem(name)

    def _selectedFilterChanged(self):
        self.selectedFilterChanged.emit(self.ui.filterListWidget.currentItem().text())

    def _addFilter(self):
        self.onAddFilter.emit(self.ui.filterListWidget.currentItem().text())

    def _reloadFilter(self):
        self.controller.reload_filter(self.ui.filterListWidget.currentItem().text())
