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
from SeaGoatVision.client.qt.shared_info import Shared_info
from PySide import QtCore

class WinFilterList(QtCore.QObject):
    """Allow the user to select a filter to add to the filterchain"""
    onAddFilter = QtCore.Signal(object)
    def __init__(self, controller):
        super(WinFilterList, self).__init__()
        self.controller = controller
        self.shared_info = Shared_info()
        self.shared_info.connect("filterchain_edit_mode", self._filterchain_edit_mode)
        self.reload_ui()

    def _filterchain_edit_mode(self):
        is_edit = self.shared_info.get("filterchain_edit_mode")
        self.ui.addFilterButton.setEnabled(bool(is_edit))

    def reload_ui(self):
        self.ui = get_ui(self)
        self.ui.addFilterButton.clicked.connect(self._addFilter)
        self.ui.reloadFilterButton.clicked.connect(self._reloadFilter)
        self.ui.filterListWidget.doubleClicked.connect(self._addFilter)
        self.ui.filterListWidget.currentItemChanged.connect(self._selectedFilterChanged)
        self.reload_list_filter(self.controller.get_filter_list())

    def reload_list_filter(self, dct_filter):
        self.dct_filter = dct_filter
        lst_filter_sort = dct_filter.keys()[:]
        lst_filter_sort.sort()
        for name in lst_filter_sort:
            self.ui.filterListWidget.addItem(name)

    def _selectedFilterChanged(self):
        filter_name = self.ui.filterListWidget.currentItem().text()
        self.ui.lbl_doc.setText("Description: %s" % self.dct_filter[filter_name])

    def _addFilter(self):
        self.onAddFilter.emit(self.ui.filterListWidget.currentItem().text())

    def _reloadFilter(self):
        self.controller.reload_filter(self.ui.filterListWidget.currentItem().text())
