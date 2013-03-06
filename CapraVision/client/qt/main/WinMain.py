#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

from CapraVision.client.qt.utils import get_ui

from WinFilterSel import WinFilterSel
from WinViewer import WinViewer
from WinFilterChain import WinFilterChain
from WinFilter import WinFilter
from PySide import QtGui
from PySide import QtCore

class WinMain(QtGui.QMainWindow):
    def __init__(self, controller):
        super(WinMain, self).__init__()

        self.winViewer = None

        # create dockWidgets
        self.winFilter = WinFilter(controller)
        self.winFilterSel = WinFilterSel(controller)
        self.winFilterChain = WinFilterChain(controller, self.winFilterSel, self.addPreview)

        self.setCentralWidget(self.winFilterChain.ui)

        # connect action between dock widgets
        self.winFilterSel.onAddFilter.connect(self.winFilterChain.add_filter)
        self.winFilterChain.selectedFilterChanged.connect(self.winFilter.setFilter)

        self.ui = get_ui(self)

        self._addDockWidget()

    def _addDockWidget(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winFilter)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winFilterSel.ui)

    def _addToolBar(self):
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)

    def addPreview(self, controller, execution_name, source_name, filterchain_name, lst_filter_str):
        if self.winViewer:
            self.winViewer.quit()
            self.removeDockWidget(self.winViewer.ui)

        self.winViewer = WinViewer(controller, execution_name, source_name, filterchain_name, lst_filter_str)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winViewer.ui)

    def quit(self):
        if self.winViewer:
            self.winViewer.quit()


