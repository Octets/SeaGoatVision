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
from SeaGoatVision.commons.keys import *
from SeaGoatVision.client.qt.shared_info import Shared_info

from PySide import QtCore
from PySide import QtGui
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class WinExecution(QtCore.QObject):
    onPreviewClick = QtCore.Signal(object, object, object)
    onExecutionChanged = QtCore.Signal(object)

    def __init__(self, controller):
        super(WinExecution, self).__init__()
        self.controller = controller
        self.shared_info = Shared_info()
        self.shared_info.connect("media", self._change_media)
        self.shared_info.connect("filterchain", self._change_filterchain)

        self.mode_edit = False
        self.last_index = 0

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.newButton.clicked.connect(self.new)
        self.ui.cancelButton.clicked.connect(self.cancel)
        self.ui.executeButton.clicked.connect(self.execute)
        self.ui.previewButton.clicked.connect(self.preview)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.lstExecution.currentItemChanged.connect(self._on_selected_lstExecution_change)
        self.ui.lstExecution.itemClicked.connect(self._lst_execution_clicked)

        self._update_execution_list()
        self._mode_edit(self.mode_edit)

    def preview(self):
        # feature, if not into edit mode, we are create a new execution
        if not self.mode_edit:
            if not self.ui.lstExecution.count():
                self._mode_edit(True)
            execution_name = self.ui.txtExecution.text()
            if not execution_name:
                return
        else:
            execution_name = self.ui.txtExecution.text()

        media_name = self.ui.txtMedia.text()
        filterchain_name = self.ui.txtFilterchain.text()
        first_filterchain_name = filterchain_name
        if not filterchain_name:
            filterchain_name = get_empty_filterchain_name()
        if self.mode_edit or not first_filterchain_name:
            if not self._execute(execution_name, media_name, filterchain_name):
                return
            else:
                self._lst_execution_clicked()
        self.onPreviewClick.emit(execution_name, media_name, filterchain_name)

    def execute(self):
        execution_name = self.ui.txtExecution.text()
        media_name = self.ui.txtMedia.text()
        filterchain_name = self.ui.txtFilterchain.text()
        self._execute(execution_name, media_name, filterchain_name)

    def stop(self):
        # remove an execution
        noLine = self.ui.lstExecution.currentRow()
        if noLine >= 0:
            execution_name = self.ui.txtExecution.text()
            self.controller.stop_filterchain_execution(execution_name)
            self.ui.lstExecution.takeItem(noLine)
            self._enable_stop_button(False)
        else:
            logger.critical("Bug internal system - winExecution - fix me please")

    def new(self):
        self._mode_edit(True)

    def cancel(self):
        self._mode_edit(False)
        self._on_selected_lstExecution_change()

    def get_execution_name(self):
        return self._get_selected_execution_name()

    ######################################################################
    ####################### PRIVATE FUNCTION  ############################
    ######################################################################
    def _lst_execution_clicked(self):
        execution_name = self.ui.txtExecution.text()
        filterchain_name = self.ui.txtFilterchain.text()
        self.shared_info.set("execution", execution_name)
        self.onExecutionChanged.emit(filterchain_name)

    def _on_selected_lstExecution_change(self):
        execution = self._get_selected_list(self.ui.lstExecution)
        if execution:
            self.ui.previewButton.setEnabled(True)
        else:
            self.ui.txtFilterchain.setText("")
            self.ui.txtMedia.setText("")
            self.ui.txtExecution.setText("")
            return
        self.ui.txtExecution.setText(execution)
        exec_info = self.controller.get_execution_info(execution)
        if not exec_info:
            logger.error("WinExecution Internal sync error with execution info :(")
            return
        self.ui.txtFilterchain.setText(exec_info.filterchain)
        self.ui.txtMedia.setText(exec_info.media)

    def _update_execution_list(self):
        self.ui.lstExecution.clear()
        for execution_name in self.controller.get_execution_list():
            self.ui.lstExecution.addItem(execution_name)
        contain_execution = bool(self.ui.lstExecution.count())

    def _get_selected_list(self, uiList):
        noLine = uiList.currentRow()
        if noLine >= 0:
            return uiList.item(noLine).text()
        return None

    def _is_unique_execution_name(self, execution_name):
        for noLine in range(self.ui.lstExecution.count()):
            if self.ui.lstExecution.item(noLine).text() == execution_name:
                return False
        return True

    def _execute(self, execution_name, media_name, filterchain_name):
        if not self._is_unique_execution_name(execution_name):
            QtGui.QMessageBox.warning(self.ui.centralwidget,
                                      "Wrong name",
                                      "The execution name \"%s\" already exist." % execution_name,
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False
        file_name = self.shared_info.get("path_media")
        status = self.controller.start_filterchain_execution(execution_name, media_name, filterchain_name, file_name)
        if not status:
            self.cancel()
            return False
        self.ui.lstExecution.addItem(execution_name)
        self.ui.lstExecution.setCurrentRow(self.ui.lstExecution.count() - 1)
        self._mode_edit(False)
        self.shared_info.set("start_execution", None)
        return True

    def _mode_edit(self, mode_edit):
        self.mode_edit = mode_edit
        self.ui.frameEdit.setVisible(mode_edit)
        self._clear_form(mode_edit)
        self.ui.txtExecution.setReadOnly(not mode_edit)
        self.ui.newButton.setEnabled(not mode_edit)
        self._enable_stop_button(mode_edit)
        self.ui.lstExecution.setEnabled(not mode_edit)
        if mode_edit:
            filterchain_name = self.shared_info.get("filterchain")
            if filterchain_name:
                self.ui.txtFilterchain.setText(filterchain_name)
            self.last_index += 1
            self.ui.txtExecution.setText("Execution-%d" % (self.last_index))
            media_name = self.shared_info.get("media")
            if media_name:
                self.ui.txtMedia.setText(media_name)

    def _enable_stop_button(self, mode_edit):
        self.ui.stopButton.setEnabled(bool(not mode_edit and self.ui.lstExecution.count()))

    def _get_selected_execution_name(self):
        noLine = self.ui.lstExecution.currentRow()
        if noLine >= 0:
            return self.ui.lstExecution.item(noLine).text()
        return None

    def _clear_form(self, mode_edit):
        if mode_edit:
            self.ui.txtExecution.clear()
            self.ui.txtMedia.clear()
            self.ui.txtFilterchain.clear()

    def _change_media(self):
        if self.mode_edit:
            media_name = self.shared_info.get("media")
            if media_name:
                self.ui.txtMedia.setText(media_name)

    def _change_filterchain(self):
        if self.mode_edit:
            filterchain_name = self.shared_info.get("filterchain")
            if filterchain_name:
                self.ui.txtFilterchain.setText(filterchain_name)
