#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

from WinFilterSel import WinFilterSel
from WinViewer import WinViewer
from WinFilterChain import WinFilterChain
from WinFilter import WinFilter
from PySide import QtGui
from PySide import QtCore

class WinMain(QtGui.QMainWindow):

    def __init__(self, controller, host="localhost"):
        super(WinMain, self).__init__()

        self.controller = controller
        self.dct_preview = {}
        self.ui = get_ui(self)

        # create dockWidgets
        self.winFilter = WinFilter(controller)
        self.winFilterSel = WinFilterSel(controller)
        self.winFilterChain = WinFilterChain(controller, self.winFilterSel)

        # connect action between dock widgets
        self.winFilterSel.onAddFilter.connect(self.winFilterChain.add_filter)
        self.winFilterChain.selectedFilterChanged.connect(self.winFilter.setFilter)
        self.winFilterChain.onPreviewClick.connect(self.addPreview)

        self._addDockWidget()
        self._addToolBar()
        
        self.host = host

    def _addDockWidget(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winFilter)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winFilterSel.ui)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winFilterChain.ui)

    def _addToolBar(self):
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)

    def addPreview(self, execution_name, source_name, filterchain_name, lst_filter_str):
        winviewer = WinViewer(self.controller, execution_name, source_name, filterchain_name, lst_filter_str, self.host)
        self.dct_preview[execution_name] = winviewer
        self.setCentralWidget(winviewer.ui)
        winviewer.closePreview.connect(self.removePreview)
        winviewer.closePreview.connect(self.winFilterChain.enable_preview)

    def removePreview(self, execution_name):
        viewer = self.dct_preview.get(execution_name, None)
        if viewer:
            viewer.closeEvent()
            self.removeDockWidget(viewer.ui)
            del self.dct_preview[execution_name]
        else:
            print("Don't find DockWidget %s" % execution_name)

    def quit(self):
        for viewer in self.dct_preview.values():
            viewer.closeEvent()
