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

class WinMedia(QtCore.QObject):
    def __init__(self, controller, islocal):
        super(WinMedia, self).__init__()
        self.ressource_icon_path = "SeaGoatVision/client/ressource/img/"
        self.controller = controller
        #self.islocal = islocal

        self.is_recorded = False
        self.record_icon = QIcon(self.ressource_icon_path + "RecordVideoAction.png")
        self.save_record_icon = QIcon(self.ressource_icon_path + "SaveServerImageAction.png")

        self.dct_media = None

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.recordButton.clicked.connect(self.click_record_button)
        self.ui.cbMedia.currentIndexChanged.connect(self._change_media)
        self.ui.openButton.clicked.connect(self.open_media)
        self.ui.btnplay.clicked.connect(self.play)
        self.ui.btnpause.clicked.connect(self.pause)

        self._set_record_icon()
        self._update_media()

    def _update_media(self):
        self.dct_media = self.controller.get_media_list()
        for media in self.dct_media.keys():
            self.ui.cbMedia.addItem(media)
        # TODO improve me
        pos = self.dct_media.keys().index("Webcam")
        #self.ui.cbMedia.setCurrentIndex(self.ui.cbMedia.count() - 1)
        self.ui.cbMedia.setCurrentIndex(pos)
        self._change_media()

    def _change_media(self):
        item_cbmedia = self.ui.cbMedia.currentText()
        frame_webcam = self.ui.frame_webcam
        frame_webcam.setVisible(False)
        frame_video = self.ui.frame_video
        frame_video.setVisible(False)

        media_type = self.dct_media.get(item_cbmedia, None)
        if not media_type:
            return
        if media_type == get_media_type_video_name():
            frame_video.setVisible(True)
        elif media_type == get_media_type_streaming_name():
            frame_webcam.setVisible(True)

    def click_record_button(self):
        if not self.is_recorded:
            if not self.controller.start_record(self.ui.cbMedia.currentText()):
                # TODO improve error message
                print("Error trying start record...")
            else:
               self.is_recorded = True
               self._set_record_icon()
        else:
            if not self.controller.stop_record(self.ui.cbMedia.currentText()):
                print("Error trying stop record...")
            self.is_recorded = False
            self._set_record_icon()

    def open_media(self):
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) > 0:
            self.ui.movieLineEdit.setText(filename)

    def play(self):
        self.movie.play()

    def pause(self):
        self.movie.pause()

    def _set_record_icon(self):
        if not self.is_recorded:
            self.ui.recordButton.setIcon(self.record_icon)
        else:
            self.ui.recordButton.setIcon(self.save_record_icon)

    def get_selected_media(self):
        if not self.ui.cbMedia.count():
            return "None"
        return self.ui.cbMedia.currentText()

    def get_file_path(self):
        item_cbmedia = self.ui.cbMedia.currentText()
        media_type = self.dct_media.get(item_cbmedia, None)
        if media_type != get_media_type_video_name():
            return None
        return self.ui.movieLineEdit.text()
