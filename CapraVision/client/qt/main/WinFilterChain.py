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

from PySide import QtGui
from PySide import QtCore


class WinFilterChain(QtCore.QObject):
    
    """Main window
    Allow the user to create, edit and test filter chains
    """
    
    WINDOW_TITLE = "Capra Vision"
    selectedFilterChanged = QtCore.Signal(object)
    
    def __init__(self, controller):
        super(WinFilterChain, self).__init__()
        
        self.controller = controller
                
        self.filterchain = None
        self.filename = None
        self.source = None
        self.thread = mainloop.MainLoop()
        self.thread.add_observer(self.thread_observer)
        
        self.ui = get_ui(self)
        self.loadSources()
        self.ui.sourcesComboBox.currentIndexChanged[str].connect(self.startSource)
        self.ui.filterListWidget.currentItemChanged.connect(self.onSelectedFilterchanged)
        self.ui.filterchainListWidget.currentItemChanged.connect(self.onSelectedFilterchainChanged)
        self.ui.sourcesButton.clicked.connect(self.getSourcesFilepath)
        self.ui.uploadButton.clicked.connect(self.upload)
        self.ui.editButton.clicked.connect(self.edit)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.cancelButton.clicked.connect(self.cancel)
        self.ui.deleteButton.clicked.connect(self.delete)
        self.ui.copyButton.clicked.connect(self.copy)
        self.ui.newButton.clicked.connect(self.new)
        
        self.updateFilterChainList()
        
        self._modeEdit(False)
        
        self._list_filterchain_is_selected(False)
        
    ######################################################################
    ############################# EVENT  #################################
    ######################################################################
    def open_chain(self):
        filename = QtGui.QFileDialog().getOpenFileName(filter="*.filterchain")[0]
        if filename:
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
            
    def upload(self):
        # open a file, copy the contain to the controller
        sExtension = ".filterchain"
        filename = QtGui.QFileDialog().getOpenFileName(filter="*%s" % sExtension)[0]
        if filename:
            filterchain_name = filename[filename.rfind("/") + 1:-len(sExtension)]
            if self._is_unique_filterchain_name(filterchain_name):
                f = open(filename, 'r')
                if f:
                    s_contain = "".join(f.readlines())
                    # if success, add the filter name on list widget
                    if self.controller.upload_filterchain(filterchain_name, s_contain):
                        self.ui.filterchainListWidget.addItem(filterchain_name)
                else:
                    print("Error, can't open the file : %s" % (filename))
            else:
                print("Error, this filtername already exist : %s" % filterchain_name)

    def edit(self):
        self._modeEdit(True)
        
    def cancel(self):
        self.updateFilterChainList()
        self._list_filterchain_is_selected(False)
        print("Cancel changement.")
        self._modeEdit(False)
        
    def save(self):
        oldName = self.ui.filterchainListWidget.currentItem().text()
        newName = self.ui.sourceNameLineEdit.text()
        
        lstFilter = self.get_listString_qList(self.ui.filterListWidget)
        print(lstFilter)
        
        if self.controller.edit_filterchain(oldName, newName, lstFilter):
            self.ui.filterchainListWidget.currentItem().setText(newName)
            print("Editing success")
        else:
            print("Error with saving edit.")
        
        self._modeEdit(False)
    
    def delete(self):
        self._modeEdit(True)
        noLine = self.ui.filterchainListWidget.currentRow()
        if noLine >= 0:
            filterchain_name = self.ui.filterchainListWidget.item(noLine).text()
            # security ask
            response = QtGui.QMessageBox.question(self.ui.centralwidget,
                                                  "Delete filterchain",
                                                  "Do you want to delete filterchain \"%s\"" % filterchain_name,
                                                  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if response == QtGui.QMessageBox.Yes:
                # delete the filterchain
                self.controller.delete_filterchain(filterchain_name)
                self.ui.filterchainListWidget.takeItem(noLine)
                print("Delete %s" % filterchain_name)
            else:
                print("Cancel delete %s" % filterchain_name)
        self._modeEdit(False)
        
    def copy(self):
        self.edit()
        
    def new(self):
        # find name of new filterchain
        i = 1
        filterchain_name = "new"
        while not self._is_unique_filterchain_name(filterchain_name):
            i += 1
            filterchain_name = "new - %s" % i
            
        # add new line
        self.ui.filterchainListWidget.addItem(filterchain_name)
        self.ui.filterchainListWidget.setCurrentRow(self.ui.filterchainListWidget.count() - 1)
        self.ui.sourceNameLineEdit.setText(filterchain_name)
        self.edit()
           
    def loadSources(self):
        self.ui.sourcesComboBox.clear()
        self.sources = imageproviders.load_sources()
        self.ui.sourcesComboBox.addItem('None')
        for source in self.sources.keys():            
            self.ui.sourcesComboBox.addItem(source) 
             
    def getSourcesFilepath(self):
        if self.source == None:
            return
        
        filepath = QtGui.QFileDialog.getExistingDirectory()[0]
        return filepath        
    
    def startSource(self,sourceText):
        if self.source <> None:
            imageproviders.close_source(self.source)
        if sourceText == 'None':
            return
        self.source = imageproviders.create_source(self.sources[sourceText])
        self.thread.start(self.source)
            
    def thread_observer(self,image):
        if self.filterchain <> None:
           self.filterchain.execute(image) 
           
    def updateFilterChain(self):
        self.ui.filterListWidget.clear()
        for filter in self.filterchain.filters:
            print filter.__class__
            self.ui.filterListWidget.addItem(filter.__class__.__name__)
            
    def updateFiltersList(self, filterchain_name):
        self.ui.filterListWidget.clear()
        for filter in self.controller.get_filters_from_filterchain(filterchain_name):
            self.ui.filterListWidget.addItem(filter.name)
            
    def updateFilterChainList(self):
        self.ui.filterchainListWidget.clear()
        self.ui.filterListWidget.clear()
        self.ui.sourceNameLineEdit.clear()
        for filterlist in self.controller.list_filterchain():
            self.ui.filterchainListWidget.addItem(filterlist)
            
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
    
    def onSelectedFilterchainChanged(self):
        # only if filterchain list enabled
        #if self.ui.filterchainListWidget.isEnabled():
        filterchain_name = self._get_selected_filterchain_name()
        if filterchain_name:
            # set the filters section
            self.ui.sourceNameLineEdit.setText(filterchain_name)
            
            self.updateFiltersList(filterchain_name)
            
            self._list_filterchain_is_selected(True)
        else:
            self._list_filterchain_is_selected(False)

    ######################################################################
    ####################### PRIVATE FUNCTION  ############################
    ######################################################################
    def _is_unique_filterchain_name(self, filterchain_name):
        for noLine in range(self.ui.filterchainListWidget.count()):
            if self.ui.filterchainListWidget.item(noLine).text() == filterchain_name:
                return False
        return True
    
    def _get_selected_filterchain_name(self):
        noLine = self.ui.filterchainListWidget.currentRow()
        if noLine >= 0:
            return self.ui.filterchainListWidget.item(noLine).text()
        return None
    
    def _modeEdit(self, status = True):
        self.ui.frame_editing.setVisible(status)
        self.ui.frame_edit.setEnabled(not status)
        self.ui.sourceNameLineEdit.setReadOnly(not status)
        self.ui.filterchainListWidget.setEnabled(not status)
        
    def _list_filterchain_is_selected(self, isSelected = True):
        self.ui.editButton.setEnabled(isSelected)
        self.ui.copyButton.setEnabled(isSelected)
        self.ui.deleteButton.setEnabled(isSelected)
        
    def get_listString_qList(self, ui):
        return [ui.item(no).text() for no in range(ui.count())]
        

