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
from PySide.QtGui import QIcon
from SeaGoatVision.commun.keys import *

from PySide import QtCore

class WinSource(QtCore.QObject):
    def __init__(self, controller, islocal):
        super(WinSource, self).__init__()
        self.ressource_icon_path = "SeaGoatVision/client/ressource/img/"
        self.controller = controller
        self.islocal = islocal

        self.is_recorded = False
        self.record_icon = QIcon(self.ressource_icon_path + "RecordVideoAction.png")
        self.save_record_icon = QIcon(self.ressource_icon_path + "SaveServerImageAction.png")

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.recordButton.clicked.connect(self.click_record_button)
        # disable local media
        self.ui.rbtnImage.setEnabled(self.islocal)
        self.ui.rbtnImageFolder.setEnabled(self.islocal)
        self.ui.rbtnVideo.setEnabled(self.islocal)

        self._set_record_icon()

    def click_record_button(self):
        if not self.is_recorded:
            if not self.controller.start_record(get_source_camera_name()):
                # TODO improve error message
                print("Error trying start record...")
            else:
               self.is_recorded = True
               self._set_record_icon()
        else:
            if not self.controller.stop_record(get_source_camera_name()):
                print("Error trying stop record...")
            self.is_recorded = False
            self._set_record_icon()

    def _set_record_icon(self):
        if not self.is_recorded:
            self.ui.recordButton.setIcon(self.record_icon)
        else:
            self.ui.recordButton.setIcon(self.save_record_icon)

    def get_selected_media(self):
        if self.ui.rbtnImage.isChecked():
            return get_source_image_name()
        elif self.ui.rbtnImageFolder.isChecked():
            return get_source_image_folder_name()
        elif self.ui.rbtnVideo.isChecked():
            return get_source_video_name()
        elif self.ui.rbtnCamera.isChecked():
            return get_source_camera_name()
        return "None"
