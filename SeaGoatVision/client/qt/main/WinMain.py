#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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
from WinRecHistoric import WinRecHistoric
from WinFilterParam import WinFilterParam
from WinMediaParam import WinMediaParam
#WIP
from WinDebugKeyz import WinDebugKeyz
from PySide import QtGui
from PySide import QtCore
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class WinMain(QtGui.QMainWindow):
    def __init__(self, controller, subscriber,
                 host="localhost", islocal=False):
        super(WinMain, self).__init__()

        self.host = host
        self.controller = controller
        self.subscriber = subscriber
        self.dct_preview = {}
        self.ui = get_ui(self)
        self.uid_iter = 0
        self.id = -1
        self.toolbar = None

        # default maximize Qt
        self.showMaximized()

        # create dockWidgets
        self.win_filter_param = WinFilterParam(controller, subscriber)
        self.win_rec_historic = WinRecHistoric(controller, subscriber)
        self.win_media_camera = WinMediaParam(controller, subscriber)
        self.win_filter_list = WinFilterList(controller)
        self.win_media = WinMedia(controller, subscriber)
        self.win_execution = WinExecution(controller, subscriber)
        self.win_filter_chain = WinFilterChain(controller)
        self.win_main_viewer = WinMainViewer()

        #WIP
        self.win_debug_keyz = WinDebugKeyz(controller, subscriber)

        # Add default widget
        self.show_win_filter(first_time=True)
        self.show_win_filterlist(first_time=True)
        self.show_win_filterchain(first_time=True)
        self.show_win_media(first_time=True)
        self.show_win_execution(first_time=True)
        self.show_win_camera(first_time=True)
        self.show_win_rec_historic(first_time=True)
        self.show_win_debug_keyz(first_time=True)

        if self.win_debug_keyz.ui:
            print "ninja style"
        else:
            print "doctor style"

        # Tabify dockwidget
        self.tabifyDockWidget(
            self.win_media.ui,
            self.win_rec_historic.ui
        )
        self.tabifyDockWidget(
            self.win_media.ui,
            self.win_media_camera.ui
        )
        self.tabifyDockWidget(
            self.win_filter_param.ui,
            self.win_filter_list.ui
        )

        # Signal
        self.win_filter_list.onAddFilter.connect(
            self.win_filter_chain.add_filter)
        self.ui.btnMedia.clicked.connect(self.show_win_media)
        self.ui.btnFilterChain.clicked.connect(self.show_win_filterchain)
        self.ui.btnFilterList.clicked.connect(self.show_win_filterlist)
        self.ui.btnExecution.clicked.connect(self.show_win_execution)
        self.ui.btnCamera.clicked.connect(self.show_win_camera)
        self.ui.btnParam.clicked.connect(self.show_win_filter)
        self.ui.btnRecHistoric.clicked.connect(self.show_win_rec_historic)
        self.ui.btnDebugKeyz.clicked.connect(self.show_win_debug_keyz)
        self.win_execution.onPreviewClick.connect(self.add_preview)

        self._add_tool_bar()
        self._add_menu_bar()

        self.setCentralWidget(self.win_main_viewer.ui)
        self.subscriber.start()

    def _add_tool_bar(self):
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)

    def show_win_filterchain(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_filter_chain.ui)
            self.win_filter_chain.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
            self.win_filter_chain.ui)

    def show_win_execution(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_execution.ui)
            self.win_execution.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
            self.win_execution.ui)

    def show_win_filterlist(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_filter_list.ui)
            self.win_filter_list.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            self.win_filter_list.ui)

    def show_win_filter(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_filter_param.ui)
            self.win_filter_param.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            self.win_filter_param.ui)

    def show_win_rec_historic(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_rec_historic.ui)
            self.win_rec_historic.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            self.win_rec_historic.ui)

    def show_win_debug_keyz(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_debug_keyz.ui)
            self.win_debug_keyz.reload_ui()
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.win_debug_keyz.ui)

    def show_win_camera(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_media_camera.ui)
            self.win_media_camera.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            self.win_media_camera.ui)

    def show_win_media(self, first_time=False):
        if not first_time:
            self.removeDockWidget(self.win_media.ui)
            self.win_media.reload_ui()
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            self.win_media.ui)

    def add_preview(self, execution_name, media_name, filterchain_name):
        winviewer = WinViewer(
            self.controller,
            self.subscriber,
            execution_name,
            media_name,
            filterchain_name,
            self.host,
            self.uid_iter)
        self.dct_preview[self.uid_iter] = winviewer
        self.uid_iter += 1
        self.win_main_viewer.grid.addWidget(winviewer.ui)
        winviewer.closePreview.connect(self.remove_preview)

    def remove_preview(self, uid):
        viewer = self.dct_preview.get(uid, None)
        if viewer:
            viewer.closeEvent()
            # self.WinMainViewer.grid.removeWidget(viewer.ui)
            self.removeDockWidget(viewer.ui)
            del self.dct_preview[uid]
        else:
            logger.error("Don't find DockWidget on uid %s" % uid)

    def quit(self):
        for viewer in self.dct_preview.values():
            viewer.closeEvent()
        self.win_media.stop()
        self.subscriber.stop()

    def _add_menu_bar(self):
        action_reconnect_seagoat = QtGui.QAction("Reconnect to server", self)
        action_reconnect_seagoat.setEnabled(False)
        # actionReloadWidget = QtGui.QAction("Reload widget", self)
        # actionReloadWidget.setEnabled(False)
        action_quit = QtGui.QAction("Quit", self)
        action_quit.triggered.connect(self.close)
        menu_file = QtGui.QMenu("File")
        menu_file.addAction(action_reconnect_seagoat)
        # menuFile.addAction(actionReloadWidget)
        menu_file.addAction(action_quit)
        menu_bar = self.menuBar()
        menu_bar.addMenu(menu_file)