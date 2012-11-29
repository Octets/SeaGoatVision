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

#from CapraVision import chain
#from CapraVision import sources
#from CapraVision import filters

from WinFilterSel import WinFilterSel
from WinMapper import WinMapper
from WinViewer import WinViewer
from WinExec import WinExec
from PySide import QtGui
from PySide import QtCore


class WinFilterChain:
    """Main window
    Allow the user to create, edit and test filter chains
    """
    
    WINDOW_TITLE = "Capra Vision"

    def __init__(self):
        
        self.filterchain = None
        self.filename = None
        self.ui = get_ui(self,)
       
    def new_chain(self):
        self.filterchain = filterchain.FilterChain()
        self.filterchain.add_filter_observer(self.updateFilterChain)

    def save_chain(self):
        if self.filename == None:
            self.save_chain_as()
        if self.filterchain is not None:
            filterchain.write(self.filename,self.filterchain)
        else:
            QtGui.QMessageBox.warning(self.ui,"filterchain","filterchain is null.")
        
    def save_chain_as(self):
        filename = QtGui.QFileDialog.getSaveFileName()[0]
        if len(filename)>0:
            self.filename = filename
            self.save_chain()
    
    
    
    def add_filter(self,filter):
        if self.filterchain is not None:
            self.filterchain.add_filter(filter)
            print filter
        else:
            QtGui.QMessageBox.warning(self.ui,"filterChain","filterchain is null.")
            
    def updateFilterChain(self):
        self.ui.filterListWidget.clear()
        for filter in self.filterchain.filters:
            print filter.__class__
            self.ui.filterListWidget.addItem(filter.__class__.__name__)
            
            

