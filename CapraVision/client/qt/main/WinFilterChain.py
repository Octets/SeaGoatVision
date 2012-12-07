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
from CapraVision.server.core import mainloop
from CapraVision.server import imageproviders

#from CapraVision import chain
#from CapraVision import sources
#from CapraVision import filters

from WinFilterSel import WinFilterSel
from WinMapper import WinMapper
from WinViewer import WinViewer
from WinExec import WinExec
from PySide import QtGui
from PySide import QtCore


class WinFilterChain(QtCore.QObject):
    
    """Main window
    Allow the user to create, edit and test filter chains
    """
    
    WINDOW_TITLE = "Capra Vision"
    selectedFilterChanged = QtCore.Signal(object)
    
    def __init__(self):
        super(WinFilterChain, self).__init__() 
                
        self.filterchain = None
        self.filename = None
        self.source = None
        self.thread = mainloop.MainLoop()
        self.thread.add_observer(self.thread_observer)
        
        self.ui = get_ui(self)
        self.loadSources()
        self.ui.sourcesComboBox.currentIndexChanged[str].connect(self.startSource)
        self.ui.filterListWidget.currentItemChanged.connect(self.onSelectedFilterchanged)
        #self.ui.filepathButton.clicked.connect(self.getSourcesFilepath())
    
    def open_chain(self):
        filename = QtGui.QFileDialog.getOpenFileName()[0]
        if len(filename)>0:
            self.filename = filename
            self.filterchain = filterchain.read(filename)
            self.filterchain.add_filter_observer(self.updateFilterChain)
            self.ui.sourceNameLineEdit.setText(self.filename)
            self.updateFilterChain()
       
    def new_chain(self):
        self.filename = None
        self.filterchain = filterchain.FilterChain()
        self.filterchain.add_filter_observer(self.updateFilterChain)
        self.updateFilterChain()
        self.ui.sourceNameLineEdit.setText("<new>")

    def save_chain(self):
        if self.filename == None:
            if not self.save_chain_as():
                return
        if self.filterchain is not None and self.filename is not None:
            filterchain.write(self.filename,self.filterchain)
        else:
            QtGui.QMessageBox.warning(self.ui,"filterchain","filterchain is null.")
        
    def save_chain_as(self):
        filename = QtGui.QFileDialog.getSaveFileName()[0]        
        if len(filename)>0:
            self.filename = filename
            self.ui.sourceNameLineEdit.setText(self.filename)
            self.save_chain()
            return True
        return False     
    
    def add_filter(self,filter):
        if self.filterchain is not None:
            self.filterchain.add_filter(filter)            
        else:
            QtGui.QMessageBox.warning(self.ui,"filterChain","filterchain is null.")
    
    def remove_filter(self):
        if self.filterchain is not None:
            filter = self._getSelectedFilter()
            self.filterchain.remove_filter(filter)
            print filter
        else:
            QtGui.QMessageBox.warning(self.ui,"filterChain","filterchain is null.")
            
           
    def loadSources(self):
        self.ui.sourcesComboBox.clear()
        self.sources = imageproviders.load_sources()
        self.ui.sourcesComboBox.addItem("None")
        for source in self.sources.keys():            
            self.ui.sourcesComboBox.addItem(source) 
             
    def getSourcesFilepath(self):
        if self.sources == None:
            return
        filepath = QtGui.QFileDialog.getExistingDirectory()[0]
        return filepath        
    
    def startSource(self,source):
        if self.source <> None:
            imageproviders.close_source(self.source)
        self.source = imageproviders.create_source(self.sources[source])
        self.thread.start(self.source)
            
    def thread_observer(self,image):
        if self.filterchain <> None:
           self.filterchain.execute(image) 
           
    def updateFilterChain(self):
        self.ui.filterListWidget.clear()
        for filter in self.filterchain.filters:
            print filter.__class__
            self.ui.filterListWidget.addItem(filter.__class__.__name__)
            
    def _getSelectedFilter(self):
        filterName = self.ui.filterListWidget.currentRow()
        if filterName == "":
            return None
        return self.filterchain.filters[filterName]
    
    def moveUpSelectedFilter(self):
        filter = self._getSelectedFilter()
        if filter == None:
            return
        self.filterchain.move_filter_up(filter)
    
    def moveDownSelectedFilter(self):
        filter = self._getSelectedFilter()
        if filter == None:
            return
        self.filterchain.move_filter_down(filter)
        
    def deleteSelectedFilter(self):
        filter = self._getSelectedFilter()
        if filter == None:
            return
        self.filterchain.remove_filter(filter)
    
    def onSelectedFilterchanged(self):
        filter = self._getSelectedFilter()
        if filter <> None:
            self.selectedFilterChanged.emit(filter)
    
        
           
           

