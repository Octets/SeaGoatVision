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

from PySide import QtCore, QtGui
from SeaGoatVision.commons import log
import datetime

logger = log.get_logger(__name__)


class WinRecHistoric(QtCore.QObject):
    def __init__(self, controller, subscriber):
        super(WinRecHistoric, self).__init__()
        self.ui = None
        self.controller = controller
        self.subscriber = subscriber
        self.shared_info = SharedInfo()
        self.reload_ui()

        self.subscriber.subscribe(keys.get_key_lst_rec_historic(),
                                  self.update_record)

    def reload_ui(self):
        self.ui = get_ui(self)
        self.refresh_list()

    def refresh_list(self):
        lst_record = self.controller.get_lst_record_historic()
        for item in lst_record:
            self.update_record(item)

    def update_record(self, data):
        if not ("time" in data and "media_name" in data and "path" in data):
            return
        table = self.ui.tableRecord
        no_row = table.rowCount()
        table.insertRow(no_row)
        date = datetime.datetime.fromtimestamp(data.get("time"))
        str_date = date.strftime('%Y-%m-%d %H:%M:%S')
        table.setItem(no_row, 0, QtGui.QTableWidgetItem(str_date))
        table.setItem(no_row, 1,
                      QtGui.QTableWidgetItem(data.get("media_name")))
        table.setItem(no_row, 2, QtGui.QTableWidgetItem(data.get("path")))
