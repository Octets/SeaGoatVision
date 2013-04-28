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

from WinFilterList import WinFilterList
from WinSource import WinSource
from WinViewer import WinViewer
from WinFilterChain import WinFilterChain
from WinExecution import WinExecution
from WinFilter import WinFilter
from PySide import QtGui
from PySide import QtCore

class WinMain(QtGui.QMainWindow):

    def __init__(self, controller, host="localhost", islocal=False):
        super(WinMain, self).__init__()

        self.host = host
        self.controller = controller
        self.dct_preview = {}
        self.ui = get_ui(self)

        # create dockWidgets
        self.winFilter = WinFilter(self.controller)
        self.winFilterList = WinFilterList(self.controller)
        self.winSource = WinSource(self.controller, islocal)
        self.winExecution = WinExecution(self.controller, self.winSource)
        self.winFilterChain = WinFilterChain(self.controller, self.winFilterList, self.winSource, self.winExecution)

        # Add default widget
        self.show_win_filter()
        self.show_win_filterlist(first_time=True)
        self.show_win_filterchain(first_time=True)
        self.show_win_source(first_time=True)
        self.show_win_execution(first_time=True)
        # exception
        self.winFilterList.onAddFilter.connect(self.winFilterChain.add_filter)

        self._addToolBar()

    def _addToolBar(self):
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)
        self.ui.btnSource.clicked.connect(self.show_win_source)
        self.ui.btnFilterChain.clicked.connect(self.show_win_filterchain)
        self.ui.btnFilterList.clicked.connect(self.show_win_filterlist)
        self.ui.btnExecution.clicked.connect(self.show_win_execution)

    def show_win_filterchain(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winFilterChain.ui)
            self.winFilterChain.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winFilterChain.ui)
        self.winFilterChain.selectedFilterChanged.connect(self.winFilter.setFilter)
        self.winFilterChain.selectedFilterChainChanged.connect(self.winExecution.set_filterchain)

    def show_win_execution(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winExecution.ui)
            self.winExecution.reload_ui()
        self.winExecution.onPreviewClick.connect(self.addPreview)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winExecution.ui)

    def show_win_filterlist(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winFilterList.ui)
            self.winFilterList.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winFilterList.ui)
        self.winFilterList.onAddFilter.connect(self.winFilterChain.add_filter)

    def show_win_filter(self):
        self.winFilter.setFeatures(QtGui.QDockWidget.DockWidgetMovable or QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winFilter)

    def show_win_source(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winSource.ui)
            self.winSource.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winSource.ui)

    def addPreview(self, execution_name, source_name, filterchain_name):
        # TODO create signal to share the filter list to WinViewer
        winviewer = WinViewer(self.controller, execution_name, source_name, filterchain_name, self.host)
        self.dct_preview[execution_name] = winviewer
        self.setCentralWidget(winviewer.ui)
        winviewer.closePreview.connect(self.removePreview)

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
