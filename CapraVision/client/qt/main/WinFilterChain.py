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

from PySide import QtGui
from PySide import QtCore

class WinFilterChain(QtCore.QObject):

    """Main window
    Allow the user to create, edit and test filter chains
    """

    WINDOW_TITLE = "Capra Vision"
    selectedFilterChanged = QtCore.Signal(object)

    def __init__(self, controller, qtWidgetFilterSelect, addPreviewCall):
        super(WinFilterChain, self).__init__()

        self.controller = controller
        self.qtWidgetFilterSelect = qtWidgetFilterSelect

        self.ui = get_ui(self)
        self.ui.filterListWidget.currentItemChanged.connect(self.onSelectedFilterchanged)
        self.ui.filterchainListWidget.currentItemChanged.connect(self.onSelectedFilterchainChanged)
        self.ui.uploadButton.clicked.connect(self.upload)
        self.ui.editButton.clicked.connect(self.edit)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.cancelButton.clicked.connect(self.cancel)
        self.ui.deleteButton.clicked.connect(self.delete)
        self.ui.copyButton.clicked.connect(self.copy)
        self.ui.newButton.clicked.connect(self.new)
        self.ui.upButton.clicked.connect(self.moveUpSelectedFilter)
        self.ui.downButton.clicked.connect(self.moveDownSelectedFilter)
        self.ui.removeButton.clicked.connect(self.remove_filter)
        self.ui.previewButton.clicked.connect(self.add_preview)

        self.updateFilterChainList()

        self._modeEdit(False)
        self._list_filterchain_is_selected(False)
        self.ui.frame_filter_edit.setEnabled(False)

        self.lastRowFilterChainSelected = 0
        
        self.addPreviewCall = addPreviewCall
        
        self.updateSources()

    ######################################################################
    #############################  SIGNAL  ###############################
    ######################################################################
    def add_preview(self):
        source_name = self.ui.sourcesComboBox.currentText()
        filterchain_name = self.ui.sourceNameLineEdit.text()
        lst_filter = self._get_listString_qList(self.ui.filterListWidget)
        self.addPreviewCall(self.controller, "Execution", source_name, filterchain_name, lst_filter)
        
    def add_filter(self, filter_name):
        if filter_name:
            self.ui.filterListWidget.addItem(filter_name)

    def remove_filter(self):
        self.ui.filterListWidget.takeItem(self.ui.filterListWidget.currentRow())

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
        self.lastRowFilterChainSelected = self.ui.filterchainListWidget.currentRow()
        self._modeEdit(True)

    def cancel(self):
        self.updateFilterChainList()
        self._list_filterchain_is_selected(False)
        self.ui.filterchainListWidget.setCurrentRow(self.lastRowFilterChainSelected)
        self._modeEdit(False)
        print("Cancel changement.")

    def save(self):
        newName = self.ui.sourceNameLineEdit.text()
        oldName = self.ui.filterchainListWidget.currentItem().text()
        # validate new name
        newName = newName.strip()
        if newName != oldName and not self._is_unique_filterchain_name(newName):
            QtGui.QMessageBox.warning(self.ui.centralwidget,
                                      "Wrong name",
                                      "The filtername \"%s\" already exist." % newName,
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return
        
        self.ui.sourceNameLineEdit.setText(newName)
        
        lstFilter = self._get_listString_qList(self.ui.filterListWidget)

        if self.controller.edit_filterchain(oldName, newName, lstFilter):
            self.ui.filterchainListWidget.currentItem().setText(newName)
            print("Editing success on filterchain %s" % newName)
        else:
            print("Error with saving edit on filterchain %s." % newName)

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

        # we copy the seleted filterchain
        noRow = self.ui.filterchainListWidget.currentRow()
        filterchain_name_temp = self.ui.filterchainListWidget.item(noRow).text() + " - copy"

        # find name of copy filterchain
        i = 1
        filterchain_name = filterchain_name_temp
        while not self._is_unique_filterchain_name(filterchain_name):
            i += 1
            filterchain_name = filterchain_name_temp + "- %s" % i

        # add copy line
        lstFiltreStr = self._get_listString_qList(self.ui.filterListWidget)
        self.ui.filterchainListWidget.insertItem(noRow + 1, filterchain_name)
        self.ui.filterchainListWidget.setCurrentRow(noRow + 1)
        self.ui.sourceNameLineEdit.setText(filterchain_name)

        for item in lstFiltreStr:
             self.ui.filterListWidget.addItem(item)


    def new(self):
        self.edit()

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

        self.ui.filterListWidget.clear()

    def updateFiltersList(self, filterchain_name):
        self.ui.filterListWidget.clear()
        for filter in self.controller.get_filter_list_from_filterchain(filterchain_name):
            self.ui.filterListWidget.addItem(filter.name)

    def updateFilterChainList(self):
        self.ui.filterchainListWidget.clear()
        self.ui.filterListWidget.clear()
        self.ui.sourceNameLineEdit.clear()
        for filterlist in self.controller.get_filterchain_list():
            self.ui.filterchainListWidget.addItem(filterlist.name)

    def moveUpSelectedFilter(self):
        self._move_curent_item_on_qtList(self.ui.filterListWidget, -1)

    def moveDownSelectedFilter(self):
        self._move_curent_item_on_qtList(self.ui.filterListWidget, 1)

    def onSelectedFilterchanged(self):
        self.ui.frame_filter_edit.setEnabled(self._get_selected_filter_name() is not None)

    def onSelectedFilterchainChanged(self):
        filterchain_name = self._get_selected_filterchain_name()
        if filterchain_name:
            # set the filters section
            self.ui.sourceNameLineEdit.setText(filterchain_name)

            self.updateFiltersList(filterchain_name)

            self._list_filterchain_is_selected(True)
        else:
            self._list_filterchain_is_selected(False)

    ######################################################################
    ######################## SOURCE FUNCTION  ############################
    ######################################################################
    def updateSources(self):
        self.ui.sourcesComboBox.clear()
        self.ui.sourcesComboBox.addItem('None')
        for source in self.controller.get_source_list():
            self.ui.sourcesComboBox.addItem(source)
        
        # I know the final item is the webcam
        self.ui.sourcesComboBox.setCurrentIndex(self.ui.sourcesComboBox.count() - 1)

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

    def _get_selected_filter_name(self):
        noLine = self.ui.filterListWidget.currentRow()
        if noLine >= 0:
            return self.ui.filterListWidget.item(noLine).text()
        return None

    def _modeEdit(self, status = True):
        self.ui.frame_editing.setVisible(status)
        self.ui.frame_filter_edit.setVisible(status)
        self.qtWidgetFilterSelect.ui.addFilterButton.setEnabled(status)
        self.ui.frame_edit.setEnabled(not status)
        self.ui.sourceNameLineEdit.setReadOnly(not status)
        self.ui.filterchainListWidget.setEnabled(not status)
        self.ui.previewButton.setEnabled(not status)

    def _list_filterchain_is_selected(self, isSelected = True):
        self.ui.editButton.setEnabled(isSelected)
        self.ui.copyButton.setEnabled(isSelected)
        self.ui.deleteButton.setEnabled(isSelected)
        self.ui.previewButton.setEnabled(isSelected)

    def _get_listString_qList(self, ui):
        return [ui.item(no).text() for no in range(ui.count())]

    def _move_curent_item_on_qtList(self, ui, nbLine):
        # take the action if nbLine is different of 0 and the limit is correct
        if nbLine:
            noRow = ui.currentRow()
            newNoRow = noRow + nbLine
            if 0 <= newNoRow < ui.count():
                # remove and add to move the item
                item = ui.takeItem(noRow)
                ui.insertItem(newNoRow, item)
                ui.setCurrentRow(newNoRow)



