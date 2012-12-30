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

from CapraVision.server import imageproviders

from WinFilterSel import WinFilterSel
from WinViewer import WinViewer
from WinFilterChain import WinFilterChain
from WinFilter import WinFilter
from PySide import QtGui
from PySide import QtCore

class WinMain(QtGui.QMainWindow):
    def __init__(self, controller):
        super(WinMain,self).__init__()
        
        self.source_list = imageproviders.load_sources()
        
        #create dockWidgets
        self.winFilter = WinFilter()
        self.winFilterSel = WinFilterSel()
        self.winFilterChain = WinFilterChain(controller, self.winFilterSel)
          
        self.setCentralWidget(self.winFilterChain.ui)      
         
        #connect action between dock widgets       
        self.winFilterSel.onAddFilter.connect(self.winFilterChain.add_filter)       
        self.winFilterChain.selectedFilterChanged.connect(self.winFilter.setFilter)
        
        self._addToolBar() 
        self._addDockWidget()
        self._connectMainButtonsToWinFilterChain()         
    
    def _connectMainButtonsToWinFilterChain(self):
        self.ui.previewButton.clicked.connect(self.addPreview)
        
    def _addDockWidget(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self.winFilter)        
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self.winFilterSel.ui)
        
    def _addToolBar(self):
        self.ui = get_ui(self)
        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)
        for widget in self.ui.children():
            if isinstance(widget, QtGui.QToolButton):
                self.toolbar.addWidget(widget)
            
    def addPreview(self):
        if not self.winFilterChain.filterchain:
            return
        self.winViewer = WinViewer(self.winFilterChain.filterchain)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,self.winViewer.ui)
        
    
