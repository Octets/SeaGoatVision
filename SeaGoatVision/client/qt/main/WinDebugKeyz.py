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
import json

from SeaGoatVision.client.qt.utils import get_ui
from SeaGoatVision.client.qt.shared_info import SharedInfo
from SeaGoatVision.commons import keys
from PySide.QtGui import QIcon

from PySide.QtCore import Qt
from PySide import QtCore, QtGui
from SeaGoatVision.commons import log
import datetime

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
        self.mode_edit = False
        self.last_index = 0
        self.count_keys = 0

        self.subscriber.subscribe(keys.get_key_count(), self.update_record_table)

    def reload_ui(self):
        self.ui = get_ui(self)
        self.refresh_list()

    def refresh_list(self):
        # TODO refresh list from server data
        self.count_keys = self.controller.get_count_keys()
        data = {"keys": self.count_keys}
        json_data = json.dumps(data)
        self.update_record_table(json_data)

    def update_record_table(self, json_data):
        # TODO DATA[socket, private key, public key]
        data = json.loads(json_data)
        values = data.get("keys", None)
        table = self.ui.tableRecord
        for value in values:
            item = table.findItems(str(value), Qt.MatchExactly)
            if not item:
                no_row = table.rowCount()
                table.insertRow(no_row)
                table.setItem(no_row, 0, QtGui.QTableWidgetItem(str(value)))
                table.setItem(no_row, 1, QtGui.QTableWidgetItem(str(values[value])))
            else:
                table.setItem(item[0].row(), 1, QtGui.QTableWidgetItem(str(values[value])))
