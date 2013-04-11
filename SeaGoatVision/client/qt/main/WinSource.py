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

class WinSource(QtCore.QObject):
    def __init__(self, controller, islocal):
        super(WinSource, self).__init__()
        self.controller = controller
        self.islocal = islocal

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        # disable local media
        self.ui.rbtnImage.setEnabled(self.islocal)
        self.ui.rbtnImageFolder.setEnabled(self.islocal)
        self.ui.rbtnVideo.setEnabled(self.islocal)

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