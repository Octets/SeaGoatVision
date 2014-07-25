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
        # eye icon taken from : http://www.iconspedia.com/icon/eye-icon-49269.html
        #
        # Part of: Mono General 4 icon pack
        # Author: Custom Icon Design, http://www.customicondesign.com/
        # License: Free for non commercial use.
        # Maximum Size Available: 256x256 px
        # Comments: 0 Comments
        # Public Tags:
        # Stats: 137 downloads, 1246 views, 0 Favs
        self.resource_icon_path = "SeaGoatVision/client/resource/img/"

        #self.subscriber.subscribe(keys.get_key_lst_rec_historic(),
        #                         self.update_record)

    def reload_ui(self):
        self.ui = get_ui(self)
        #self.refresh_list()

    def refresh_list(self):
        #TODO refresh list from server data
        pass
        #lst_record = self.controller.get_lst_record_historic()
        #for item in lst_record:
        #    self.update_record(item)

    def update_record(self, data):
        pass
        #TODO DATA[socket, private key, public key]
        #if not ("time" in data and "media_name" in data and "path" in data):
        #    return
        #table = self.ui.tableRecord
        #no_row = table.rowCount()
        #table.insertRow(no_row)
        #date = datetime.datetime.fromtimestamp(data.get("time"))
        #str_date = date.strftime('%Y-%m-%d %H:%M:%S')
        #table.setItem(no_row, 0, QtGui.QTableWidgetItem(str_date))
        #table.setItem(no_row, 1,
        #              QtGui.QTableWidgetItem(data.get("media_name")))
        #table.setItem(no_row, 2, QtGui.QTableWidgetItem(data.get("path")))
        #table.setItem(no_row, 3, QtGui.QTableWidgetItem())
        #table.item(no_row, 3).setIcon(
        #    QIcon(self.resource_icon_path + "PreviewAction.png"))
        #table.item(no_row, 3).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        #table.itemDoubleClicked.connect(self.preview)

    def preview(self, item):
        pass
        #if item.column() == 3:
        #    table = self.ui.tableRecord
        #    file_name = table.item(item.row(), 2).text()
        #    self.shared_info.set(
        #        SharedInfo.GLOBAL_PATH_MEDIA, file_name)
        #    self.shared_info.set(
        #        SharedInfo.GLOBAL_HIST_REC_PATH_MEDIA, file_name)