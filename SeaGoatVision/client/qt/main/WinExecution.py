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
from SeaGoatVision.commun.keys import *

from PySide import QtCore
from PySide import QtGui

# TODO missing change textbox value when exectionList selected item change

class WinExecution(QtCore.QObject):
    onPreviewClick = QtCore.Signal(object, object, object)

    def __init__(self, controller, winSource):
        super(WinExecution, self).__init__()
        self.controller = controller
        self.winSource = winSource

        self.mode_edit = False
        self.last_index = -1
        self.filterchain_txt = ""

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.newButton.clicked.connect(self.new)
        self.ui.cancelButton.clicked.connect(self.cancel)
        self.ui.executeButton.clicked.connect(self.execute)
        self.ui.previewButton.clicked.connect(self.preview)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.lstExecution.currentItemChanged.connect(self._on_selected_lstExecution_change)

        self.ui.txtSource.setReadOnly(True)
        self.ui.txtFilterchain.setReadOnly(True)
        self._mode_edit(self.mode_edit)
        self._update_execution_list()

    def set_filterchain(self, filterchain):
        self._enable_execution_button(True)
        self.filterchain_txt = filterchain
        if self.mode_edit:
            self.ui.txtFilterchain.setText(filterchain)

    def preview(self):
        # feature, if list is empty, we are create a new execution
        if not self.ui.lstExecution.count():
            self._mode_edit(True)
        execution_name = self.ui.txtExecution.text()
        source_name = self.ui.txtSource.text()
        filterchain_name = self.ui.txtFilterchain.text()
        if self.mode_edit:
            if not self._execute(execution_name, source_name, filterchain_name):
                return
        self.onPreviewClick.emit(execution_name, source_name, filterchain_name)

    def execute(self):
        execution_name = self.ui.txtExecution.text()
        source_name = self.ui.txtSource.text()
        filterchain_name = self.ui.txtFilterchain.text()
        self._execute(execution_name, source_name, filterchain_name)

    def stop(self):
        # remove an execution
        noLine = self.ui.lstExecution.currentRow()
        if noLine >= 0:
            execution_name = self.ui.txtExecution.text()
            self.controller.stop_filterchain_execution(execution_name)
            self.ui.lstExecution.takeItem(noLine)
            self._enable_stop_button(True)
            self._enable_execution_button(True)
        else:
            print("Bug internal system - winExecution - fix me please")

    def new(self):
        self._mode_edit(True)

    def cancel(self):
        self._mode_edit(False)
        self._clear_form(True)

    def get_execution_name(self):
        return self._get_selected_execution_name()

    ######################################################################
    ####################### PRIVATE FUNCTION  ############################
    ######################################################################
    def _on_selected_lstExecution_change(self):
        execution = self._get_selected_list(self.ui.lstExecution)
        if execution:
            self.ui.previewButton.setEnabled(True)
        else:
            self.ui.txtFilterchain.setText("")
            self.ui.txtSource.setText("")
            self.ui.txtExecution.setText("")
            return
        self.ui.txtExecution.setText(execution)
        exec_info = self.controller.get_execution_info(execution)
        if not exec_info:
            print("WinExecution Internal sync error with execution info :(")
        self.ui.txtFilterchain.setText(exec_info.filterchain)
        self.ui.txtSource.setText(exec_info.source)

    def _update_execution_list(self):
        self.ui.lstExecution.clear()
        for execution_name in self.controller.get_execution_list():
            self.ui.lstExecution.addItem(execution_name)
        contain_execution = bool(self.ui.lstExecution.count())
        self._enable_stop_button(contain_execution)
        # TODO fix temporary a bug, enable execute
        self._enable_execution_button(not contain_execution)

    def _get_selected_list(self, uiList):
        # TODO it's duplicated fct
        noLine = uiList.currentRow()
        if noLine >= 0:
            return uiList.item(noLine).text()
        return None

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

    def _execute(self, execution_name, source_name, filterchain_name):
        if not self._is_unique_execution_name(execution_name):
            QtGui.QMessageBox.warning(self.ui.centralwidget,
                                      "Wrong name",
                                      "The execution name \"%s\" already exist." % execution_name,
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False
        self.controller.start_filterchain_execution(execution_name, source_name, filterchain_name)
        self.ui.lstExecution.addItem(execution_name)
        self.ui.lstExecution.setCurrentRow(self.ui.lstExecution.count() - 1)
        self._mode_edit(False)
        # TODO fix temporary a bug, disable execute
        self._enable_execution_button(False)
        return True

    def _mode_edit(self, status):
        self.mode_edit = status
        self.ui.frameEdit.setVisible(status)
        self._clear_form(status)
        self.ui.txtExecution.setReadOnly(not status)
        self.ui.newButton.setEnabled(not status)
        self._enable_stop_button(not status)
        if status:
            self.ui.txtFilterchain.setText(self.filterchain_txt)
            self.ui.txtExecution.setText("Execution-01")
            self.ui.txtSource.setText(self.winSource.get_selected_media())

    def _enable_execution_button(self, status):
        # TODO fix temporary a bug, disable execute if already contain execution
        already_contain_exe = bool(self.ui.lstExecution.count())
        # with preview button
        active_button = bool(status and self.filterchain_txt)
        self.ui.newButton.setEnabled(active_button and not self.mode_edit)
        self.ui.executeButton.setEnabled(active_button and not already_contain_exe)
        # Exception, if execution list is empty, we can preview
        if not self.ui.lstExecution.count():
            active_button = True
        self.ui.previewButton.setEnabled(active_button and not already_contain_exe)

    def _enable_stop_button(self, status):
        if status and self.ui.lstExecution.count():
            self.ui.stopButton.setEnabled(True)
        else:
            self.ui.stopButton.setEnabled(False)

    def _get_selected_execution_name(self):
        noLine = self.ui.lstExecution.currentRow()
        if noLine >= 0:
            return self.ui.lstExecution.item(noLine).text()
        return None

    def _clear_form(self, status):
        if status:
            self.ui.txtExecution.clear()
            self.ui.txtSource.clear()
            self.ui.txtFilterchain.clear()