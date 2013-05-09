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

from PySide.QtGui import QFileDialog

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

        self.dct_source = None

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.recordButton.clicked.connect(self.click_record_button)
        self.ui.cbSource.currentIndexChanged.connect(self._change_source)
        self.ui.openButton.clicked.connect(self.open_media)

        self._set_record_icon()
        self._update_source()

    def _update_source(self):
        self.dct_source = self.controller.get_source_list()
        for source in self.dct_source.keys():
            self.ui.cbSource.addItem(source)
        # TODO improve me
        pos = self.dct_source.keys().index("Webcam")
        #self.ui.cbSource.setCurrentIndex(self.ui.cbSource.count() - 1)
        self.ui.cbSource.setCurrentIndex(pos)
        self._change_source()

    def _change_source(self):
        item_cbsource = self.ui.cbSource.currentText()
        frame_webcam = self.ui.frame_webcam
        frame_webcam.setVisible(False)
        frame_video = self.ui.frame_video
        frame_video.setVisible(False)

        source_type = self.dct_source.get(item_cbsource, None)
        if not source_type:
            return
        if source_type == get_source_type_video_name():
            frame_video.setVisible(True)
        elif source_type == get_source_type_streaming_name():
            frame_webcam.setVisible(True)

    def click_record_button(self):
        if not self.is_recorded:
            if not self.controller.start_record(self.ui.cbSource.currentText()):
                # TODO improve error message
                print("Error trying start record...")
            else:
               self.is_recorded = True
               self._set_record_icon()
        else:
            if not self.controller.stop_record(self.ui.cbSource.currentText()):
                print("Error trying stop record...")
            self.is_recorded = False
            self._set_record_icon()

    def open_media(self):
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) > 0:
            self.ui.movieLineEdit.setText(filename)

    def _set_record_icon(self):
        if not self.is_recorded:
            self.ui.recordButton.setIcon(self.record_icon)
        else:
            self.ui.recordButton.setIcon(self.save_record_icon)

    def get_selected_media(self):
        if not self.ui.cbSource.count():
            return "None"
        return self.ui.cbSource.currentText()

    def get_file_path(self):
        item_cbsource = self.ui.cbSource.currentText()
        source_type = self.dct_source.get(item_cbsource, None)
        if source_type != get_source_type_video_name():
            return None
        return self.ui.movieLineEdit.text()
