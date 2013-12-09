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
from WinMedia import WinMedia
from WinViewer import WinViewer
from WinFilterChain import WinFilterChain
from WinExecution import WinExecution
from WinMainViewer import WinMainViewer
from WinFilter import WinFilter
from WinCamera import WinCamera
from PySide import QtGui
from PySide import QtCore
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class WinMain(QtGui.QMainWindow):

    def __init__(self, controller, subscriber, host="localhost", islocal=False):
        super(WinMain, self).__init__()

        self.host = host
        self.controller = controller
        self.subscriber = subscriber
        self.dct_preview = {}
        self.ui = get_ui(self)
        self.uid_iter = 0
        self.id = -1

        # default maximize Qt
        self.showMaximized()

        # create dockWidgets
        self.winFilter = WinFilter(self.controller, subscriber)
        self.winCamera = WinCamera(self.controller, subscriber)
        self.winFilterList = WinFilterList(self.controller)
        self.winMedia = WinMedia(self.controller)
        self.winExecution = WinExecution(self.controller, subscriber)
        self.winFilterChain = WinFilterChain(self.controller)
        self.WinMainViewer = WinMainViewer()

        # Add default widget
        self.show_win_filter(first_time=True)
        self.show_win_filterlist(first_time=True)
        self.show_win_filterchain(first_time=True)
        self.show_win_media(first_time=True)
        self.show_win_execution(first_time=True)
        self.show_win_camera(first_time=True)

        # Tabify dockwidget
        self.tabifyDockWidget(self.winMedia.ui, self.winCamera.ui)
        self.tabifyDockWidget(self.winFilter.ui, self.winFilterList.ui)

        # Signal
        self.winFilterList.onAddFilter.connect(self.winFilterChain.add_filter)
        self.ui.btnMedia.clicked.connect(self.show_win_media)
        self.ui.btnFilterChain.clicked.connect(self.show_win_filterchain)
        self.ui.btnFilterList.clicked.connect(self.show_win_filterlist)
        self.ui.btnExecution.clicked.connect(self.show_win_execution)
        self.ui.btnCamera.clicked.connect(self.show_win_camera)
        self.ui.btnParam.clicked.connect(self.show_win_filter)
        self.winExecution.onPreviewClick.connect(self.addPreview)
        self.winExecution.onExecutionChanged.connect(self.winFilterChain.select_filterchain)

        self._addToolBar()
        self._addMenuBar()

        self.setCentralWidget(self.WinMainViewer.ui)
        self.subscriber.start()

    def _addToolBar(self):
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)

    def show_win_filterchain(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winFilterChain.ui)
            self.winFilterChain.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winFilterChain.ui)

    def show_win_execution(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winExecution.ui)
            self.winExecution.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.winExecution.ui)

    def show_win_filterlist(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winFilterList.ui)
            self.winFilterList.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winFilterList.ui)

    def show_win_filter(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winFilter.ui)
            self.winFilter.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winFilter.ui)

    def show_win_camera(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winCamera.ui)
            self.winCamera.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winCamera.ui)

    def show_win_media(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.winMedia.ui)
            self.winMedia.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.winMedia.ui)

    def addPreview(self, execution_name, media_name, filterchain_name):
        winviewer = WinViewer(self.controller, self.subscriber, execution_name, media_name, filterchain_name, self.host, self.uid_iter)
        self.dct_preview[self.uid_iter] = winviewer
        self.uid_iter += 1
        self.WinMainViewer.grid.addWidget(winviewer.ui)
        winviewer.closePreview.connect(self.removePreview)

    def removePreview(self, uid):
        viewer = self.dct_preview.get(uid, None)
        if viewer:
            viewer.closeEvent()
            #self.WinMainViewer.grid.removeWidget(viewer.ui)
            self.removeDockWidget(viewer.ui)
            del self.dct_preview[uid]
        else:
            logger.error("Don't find DockWidget on uid %s" % uid)

    def quit(self):
        for viewer in self.dct_preview.values():
            viewer.closeEvent()
        self.winMedia.stop()
        self.subscriber.stop()

    def _addMenuBar(self):
        actionReconSeaGoat = QtGui.QAction("Reconnect to server",self)
        actionReconSeaGoat.setEnabled(False)
        #actionReloadWidget = QtGui.QAction("Reload widget", self)
        #actionReloadWidget.setEnabled(False)
        actionQuit = QtGui.QAction("Quit", self)
        actionQuit.triggered.connect(self.close)
        menuFile = QtGui.QMenu("File")
        menuFile.addAction(actionReconSeaGoat)
        #menuFile.addAction(actionReloadWidget)
        menuFile.addAction(actionQuit)
        menuBar = self.menuBar()
        menuBar.addMenu(menuFile)
