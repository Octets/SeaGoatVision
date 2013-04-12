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


class WinExecution(QtCore.QObject):
    onPreviewClick = QtCore.Signal(object, object, object)
    
    def __init__(self, controller, winSource):
        super(WinExecution, self).__init__()
        self.controller = controller
        self.winSource = winSource

        self.mode_edit = False
        self.last_index = -1
        self.reload_ui()
        
        self.filterchain_txt = ""

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.newButton.clicked.connect(self.new)
        self.ui.cancelButton.clicked.connect(self.cancel)
        self.ui.executeButton.clicked.connect(self.execute)
        self.ui.previewButton.clicked.connect(self.preview)

        self.ui.txtSource.setEnabled(self.mode_edit)
        self.ui.txtFilterchain.setEnabled(self.mode_edit)
        self._mode_edit(self.mode_edit)

    def set_filterchain(self, filterchain):
        self.filterchain_txt = filterchain
        if self.mode_edit:
            self.ui.txtFilterchain.setText(filterchain)

    def preview(self):
        execution_name = self.ui.txtExecution.text()
        source_name = self.ui.txtSource.text()
        filterchain_name = self.ui.txtFilterchain.text()
        self.execute()
        self.onPreviewClick.emit(execution_name, source_name, filterchain_name)

    def execute(self):
        execution_name = self.ui.txtExecution.text()
        source_name = self.ui.txtSource.text()
        filterchain_name = self.ui.txtFilterchain.text()
        self._execute(execution_name, source_name, filterchain_name)
        self._mode_edit(False)

    def _execute(self, execution_name, source_name, filterchain_name):
        self.controller.start_filterchain_execution(execution_name, source_name, filterchain_name)

    def new(self):
        self._mode_edit(True)
        
    def cancel(self):
        self._mode_edit(False)

    def _mode_edit(self, status):
        self.mode_edit = status
        self.ui.frameEdit.setVisible(status)
        self._clear_form(status)
        self.ui.newButton.setEnabled(not status)
        self.ui.stopButton.setEnabled(not status)
        if status:
            self.ui.txtFilterchain.setText(self.filterchain_txt)
            self.ui.txtExecution.setText("Execution-01")
            self.ui.txtSource.setText(self.winSource.get_selected_media())
        
    def _clear_form(self, status):
        if status:
            self.ui.txtExecution.clear()
            self.ui.txtSource.clear()
            self.ui.txtFilterchain.clear()
        self.ui.txtExecution.setEnabled(status)