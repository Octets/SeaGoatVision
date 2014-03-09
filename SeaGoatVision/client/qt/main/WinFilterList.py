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
from SeaGoatVision.client.qt.shared_info import SharedInfo
from PySide import QtCore


class WinFilterList(QtCore.QObject):
    """Allow the user to select a filter to add to the filterchain"""
    onAddFilter = QtCore.Signal(object)

    def __init__(self, controller):
        super(WinFilterList, self).__init__()
        self.controller = controller
        self.shared_info = SharedInfo()
        self.shared_info.connect(SharedInfo.GLOBAL_FILTER_CHAIN_EDIT_MODE,
                                 self._filterchain_edit_mode)
        self.shared_info.connect(SharedInfo.GLOBAL_FILTER, self.change_filter)
        self.ui = None
        self.dct_filter = None
        self.lst_filter_sort = []
        self.reload_ui()

    def _filterchain_edit_mode(self, value):
        is_edit = value
        self.ui.addFilterButton.setEnabled(bool(is_edit))

    def reload_ui(self):
        self.ui = get_ui(self)
        self.ui.addFilterButton.clicked.connect(self._add_filter)
        self.ui.reloadFilterButton.clicked.connect(self._reload_filter)
        self.ui.filterListWidget.doubleClicked.connect(self._add_filter)
        self.ui.filterListWidget.currentItemChanged.connect(self._selected_filter_changed)
        self.reload_list_filter(self.controller.get_filter_list())

    def reload_list_filter(self, dct_filter):
        self.dct_filter = dct_filter
        self.lst_filter_sort = sorted(dct_filter.keys())
        for name in self.lst_filter_sort:
            self.ui.filterListWidget.addItem(name)

    def change_filter(self, filter_name):
        # Need to remove junk info in filter_name
        if not filter_name:
            return
        pos = filter_name.rfind("-")
        if pos:
            filter_name = filter_name[:pos]
        index = self.lst_filter_sort.index(filter_name)
        if index >= 0:
            self.ui.filterListWidget.setCurrentRow(index)

    def _selected_filter_changed(self):
        filter_name = self.ui.filterListWidget.currentItem().text()
        self.ui.lbl_doc.setText("Description: %s" % self.dct_filter[filter_name])

    def _add_filter(self):
        self.onAddFilter.emit(self.ui.filterListWidget.currentItem().text())

    def _reload_filter(self):
        filter_name = self.ui.filterListWidget.currentItem().text()
        self.controller.reload_filter(filter_name)
        self.shared_info.set(SharedInfo.GLOBAL_RELOAD_FILTER, filter_name)
