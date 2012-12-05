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
from CapraVision.server.core import filterchain

from CapraVision.server import imageproviders
from CapraVision.server.core import filterchain
from CapraVision.server.core import mainloop

from CapraVision.server.tcp_server import Server

from WinFilterSel import WinFilterSel
from WinMapper import WinMapper
from WinViewer import WinViewer
from WinExec import WinExec
from WinFilterChain import WinFilterChain
from WinViewer import WinViewer
from PySide import QtGui
from PySide import QtCore

class WinMain(QtGui.QMainWindow):
    def __init__(self):
        super(WinMain,self).__init__()
        
        self.source_list = imageproviders.load_sources()
        self.server = Server()
        self.server.start("127.0.0.1", 5030)
        
        self._addToolBar()
        
        self.winFilterChain = WinFilterChain()
        self.ui.saveButton.clicked.connect(self.winFilterChain.save_chain)
        self.ui.saveAsButton.clicked.connect(self.winFilterChain.save_chain_as)
        self.ui.createNewButton.clicked.connect(self.winFilterChain.new_chain)
        self.setCentralWidget(self.winFilterChain.ui)
        
        self.winFilterSel = WinFilterSel()       
        
        self.winFilterSel.onAddFilter.connect(self.winFilterChain.add_filter)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self.winFilterSel.ui)
        
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,WinExec().ui)
        
        self.ui.previewButton.clicked.connect(self.addPreview)
        self.ui.upButton.clicked.connect(self.winFilterChain.moveUpSelectedFilter)
        self.ui.downButton.clicked.connect(self.winFilterChain.moveDownSelectedFilter)
        
    def _addToolBar(self):
        self.ui = get_ui(self)
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)
            
    def addPreview(self):
        if self.winFilterChain.filterchain == None:
            return
        self.winViewer = WinViewer(self.winFilterChain.filterchain)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,self.winViewer.ui)
        
    
