# ! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
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
from SeaGoatVision.client.qt.shared_info import SharedInfo
from SeaGoatVision.commons import keys
from PySide.QtGui import QIcon

from PySide.QtCore import Qt
from PySide import QtCore, QtGui
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class WinDebugKeyz(QtCore.QObject):
    onPreviewClick = QtCore.Signal(object, object, object)

    def __init__(self, controller, subscriber):
        super(WinDebugKeyz, self).__init__()
        self.ui = None
        self.controller = controller
        self.subscriber = subscriber
        self.shared_info = SharedInfo()
        self.reload_ui()

        subscriber.subscribe(keys.get_key_count(), self.update_record_table)

    def reload_ui(self):
        self.ui = get_ui(self)
        self.refresh_list()

    def refresh_list(self):
        count_keys = self.controller.get_count_keys()
        self.update_record_table(count_keys)

    def update_record_table(self, dict_count_key):
        # TODO DATA[socket, private key, public key]
        table = self.ui.tableRecord
        for key, count in dict_count_key.items():
            item = table.findItems(str(key), Qt.MatchExactly)
            count_column = QtGui.QTableWidgetItem(str(count))
            if not item:
                column_key = QtGui.QTableWidgetItem(str(key))
                no_row = table.rowCount()
                table.insertRow(no_row)
                table.setItem(no_row, 0, column_key)
                table.setItem(no_row, 1, count_column)
            else:
                no_row = item[0].row()
                table.setItem(no_row, 1, count_column)
