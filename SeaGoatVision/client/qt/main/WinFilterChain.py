#! /usr/bin/env python

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
from SeaGoatVision.commons import keys
from SeaGoatVision.client.qt.shared_info import Shared_info

from PySide import QtGui
from PySide import QtCore
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class WinFilterChain(QtCore.QObject):
    """Main window
    Allow the user to create, edit and test filter chains
    """
    def __init__(self, controller):
        super(WinFilterChain, self).__init__()

        self.controller = controller
        self.lastRowFilterChainSelected = 0
        self.shared_info = Shared_info()

        self.reload_ui()

    def reload_ui(self):
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

        self.updateFilterChainList()
        self.ui.frame_filter_edit.setEnabled(False)
        self.lock_preview = False

        self.edit_mode = False
        self.mode_new = False
        self._modeEdit(False)
        self._list_filterchain_is_selected(False)

        self.shared_info.connect("media", self._update_media_default_edit)

    ######################################################################
    #############################  SIGNAL  ###############################
    ######################################################################
    def _update_media_default_edit(self, value):
        if self.edit_mode and not self.mode_new:
            return
        txt = ""
        if value != keys.get_media_file_video_name():
            txt = value
        self.ui.media_default_edit.setText(txt)

    def add_filter(self, filter_name):
        if not self.edit_mode:
            return
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
                    logger.error("Can't open the file : %s" % (filename))
            else:
                logger.error("This filtername already exist : %s" % filterchain_name)

    def edit(self):
        self.lastRowFilterChainSelected = self.ui.filterchainListWidget.currentRow()
        self._modeEdit(True)

    def cancel(self):
        self.updateFilterChainList()
        self._list_filterchain_is_selected(False)
        self.ui.filterchainListWidget.setCurrentRow(self.lastRowFilterChainSelected)
        self._modeEdit(False)
        logger.info("Cancel changement.")

    def save(self):
        newName = self.ui.filterchainEdit.text()
        oldName = self.ui.filterchainListWidget.currentItem().text()
        # validate new name
        newName = newName.strip()
        if newName != oldName and not self._is_unique_filterchain_name(newName):
            QtGui.QMessageBox.warning(self.ui.centralwidget,
                                      "Wrong name",
                                      "The filtername \"%s\" already exist." % newName,
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return

        self.ui.filterchainEdit.setText(newName)

        lstFilter = self._get_listString_qList(self.ui.filterListWidget)
        default_media = self.ui.media_default_edit.text()

        if self.controller.modify_filterchain(oldName, newName, lstFilter, default_media):
            self.ui.filterchainListWidget.currentItem().setText(newName)
            logger.info("Editing success on filterchain %s" % newName)
            self._modeEdit(False)
            self.updateFiltersList()
        else:
            logger.error("Saving edit on filterchain %s." % newName)
            self.cancel()

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
                logger.info("Delete %s" % filterchain_name)
            else:
                logger.info("Cancel delete %s" % filterchain_name)
        self._modeEdit(False)
        # update the widget
        self.onSelectedFilterchainChanged()

    def copy(self):
        self.edit()

        # we copy the selected filterchain
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
        self.ui.filterchainEdit.setText(filterchain_name)

        for item in lstFiltreStr:
            self.ui.filterListWidget.addItem(item)

    def new(self):
        self.mode_new = True
        self.edit()

        # find name of new filterchain
        i = 1
        filterchain_name = "new"
        while not self._is_unique_filterchain_name(filterchain_name):
            i += 1
            filterchain_name = "new-%s" % i

        # add new line
        self.ui.filterchainListWidget.addItem(filterchain_name)
        self.ui.filterchainListWidget.setCurrentRow(self.ui.filterchainListWidget.count() - 1)
        self.ui.filterchainEdit.setText(filterchain_name)

        self.ui.filterListWidget.clear()

    def updateFiltersList(self, filterchain_name=None):
        if not filterchain_name:
            filterchain_name = self._get_selected_filterchain_name()
        self.ui.filterListWidget.clear()

        if filterchain_name == keys.get_empty_filterchain_name():
            return

        info = self.controller.get_filterchain_info(filterchain_name)
        lst_filter = info.get("filters", None)
        if not lst_filter:
            logger.warning("Recieve empty filter list from filterchain %s" % filterchain_name)
            return
        for o_filter in lst_filter:
            name = o_filter.get("name", "")
            if name == keys.get_empty_filter_name():
                continue
            self.ui.filterListWidget.addItem(name)
        default_media = info.get("default_media", "")
        self.ui.media_default_edit.setText(default_media)

    def updateFilterChainList(self):
        self.ui.filterchainListWidget.clear()
        self.ui.filterListWidget.clear()
        self.ui.filterchainEdit.clear()
        for filterlist in self.controller.get_filterchain_list():
            self.ui.filterchainListWidget.addItem(filterlist.get("name"))
        self.ui.filterchainListWidget.addItem(keys.get_empty_filterchain_name())

    def moveUpSelectedFilter(self):
        self._move_curent_item_on_qtList(self.ui.filterListWidget, -1)

    def moveDownSelectedFilter(self):
        self._move_curent_item_on_qtList(self.ui.filterListWidget, 1)

    def onSelectedFilterchanged(self):
        filter_name = self._get_selected_filter_name()
        self.ui.frame_filter_edit.setEnabled(filter_name is not None)
        if filter_name:
            self.shared_info.set("filter", filter_name)
        else:
            self.shared_info.set("filter", None)

    def onSelectedFilterchainChanged(self):
        if self.edit_mode:
            return
        filterchain_name = self._get_selected_filterchain_name()
        if filterchain_name:
            # set the filters section
            self.ui.filterchainEdit.setText(filterchain_name)
            self.updateFiltersList(filterchain_name)
            self._list_filterchain_is_selected(True)

            filterchain_name = self._get_selected_filterchain_name()

            # Exception, don't edit or delete special empty filterchain
            self.ui.deleteButton.setEnabled(filterchain_name != keys.get_empty_filterchain_name())
            self.ui.editButton.setEnabled(filterchain_name != keys.get_empty_filterchain_name())
            self.shared_info.set("filterchain", filterchain_name)
        else:
            self._list_filterchain_is_selected(False)
            self.shared_info.set("filterchain", None)

    def get_filter_list(self):
        return self._get_listString_qList(self.ui.filterListWidget)

    def select_filterchain(self, filterchain_name):
        items = self.ui.filterchainListWidget.findItems(filterchain_name, QtCore.Qt.MatchExactly)
        if not items:
            return
        self.ui.filterchainListWidget.setCurrentItem(items[0])
        self.ui.filterListWidget.setCurrentRow(0)

    ######################################################################
    ####################### PRIVATE FUNCTION  ############################
    ######################################################################

    def _is_unique_filterchain_name(self, filterchain_name):
        for noLine in range(self.ui.filterchainListWidget.count()):
            if self.ui.filterchainListWidget.item(noLine).text() == filterchain_name:
                return False
        return True

    def _get_selected_filterchain_name(self):
        return self._get_selected_list(self.ui.filterchainListWidget)

    def _get_selected_filter_name(self):
        return self._get_selected_list(self.ui.filterListWidget)

    def _get_selected_list(self, uiList):
        noLine = uiList.currentRow()
        if noLine >= 0:
            return uiList.item(noLine).text()
        return None

    def _modeEdit(self, status=True):
        self.edit_mode = status
        self.ui.frame_editing.setVisible(status)
        self.ui.frame_editing_2.setVisible(status)
        self.ui.frame_filter_edit.setVisible(status)
        self.ui.frame_edit.setEnabled(not status)
        self.ui.filterchainEdit.setReadOnly(not status)
        self.ui.filterchainListWidget.setEnabled(not status)
        self.shared_info.set("filterchain_edit_mode", status)
        if status:
            self.ui.filterchainEdit.setFocus()
        else:
            self.mode_new = False

    def _list_filterchain_is_selected(self, isSelected=True):
        self.ui.editButton.setEnabled(isSelected)
        self.ui.copyButton.setEnabled(isSelected)
        self.ui.deleteButton.setEnabled(isSelected)

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
