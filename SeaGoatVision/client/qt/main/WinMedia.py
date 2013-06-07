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
from SeaGoatVision.client.qt.shared_info import Shared_info
from PySide.QtGui import QIcon
from SeaGoatVision.commons.keys import *
from SeaGoatVision.client.qt import config
from PySide.QtGui import QFileDialog

from PySide import QtCore

class WinMedia(QtCore.QObject):
    def __init__(self, controller):
        super(WinMedia, self).__init__()
        self.ressource_icon_path = "SeaGoatVision/client/ressource/img/"
        self.controller = controller
        self.shared_info = Shared_info()
        self.shared_info.connect("start_execution", self.set_info)

        self.is_recorded = False
        self.is_pause = False
        self.record_icon = QIcon(self.ressource_icon_path + "RecordVideoAction.png")
        self.save_record_icon = QIcon(self.ressource_icon_path + "SaveServerImageAction.png")
        self.play_icon = QIcon("/usr/share/icons/gnome/24x24/actions/player_play.png")
        self.pause_icon = QIcon("/usr/share/icons/gnome/24x24/actions/player_pause.png")

        self.dct_media = None

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.recordButton.clicked.connect(self.click_record_button)
        self.ui.cbMedia.currentIndexChanged.connect(self._change_media)
        self.ui.openDirButton.clicked.connect(self.open_directory)
        self.ui.openFileButton.clicked.connect(self.open_file)
        self.ui.btnplay.clicked.connect(self.play)
        self.ui.loopchb.clicked.connect(self.active_loop)
        self.ui.movieLineEdit.textChanged.connect(self._movie_changed)

        self._set_record_icon()
        self._set_play_icon()
        self._update_media()

    def _update_media(self):
        self.dct_media = self.controller.get_media_list()
        for media in self.dct_media.keys():
            self.ui.cbMedia.addItem(media)
        if config.default_media_selected in self.dct_media.keys():
            pos = self.dct_media.keys().index(config.default_media_selected)
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
            self.shared_info.set("media", None)
            return
        if media_type == get_media_type_video_name():
            frame_video.setVisible(True)
        elif media_type == get_media_type_streaming_name():
            frame_webcam.setVisible(True)
            self.shared_info.set("path_media", None)
        self.shared_info.set("media", self.ui.cbMedia.currentText())
        self.set_info()

    def _movie_changed(self):
        self.shared_info.set("path_media", self.ui.movieLineEdit.text())

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

    def open_directory(self):
        filename = QFileDialog.getExistingDirectory()
        if len(filename) > 0:
            self.ui.movieLineEdit.setText(filename)

    def open_file(self):
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) > 0:
            self.ui.movieLineEdit.setText(filename)

    def set_info(self):
        media_name = self.shared_info.get("media")
        if not media_name:
            return
        info = self.controller.get_info_media(media_name)
        self.ui.lblframe.setText("/%s" % info.get("nb_frame"))
        self.ui.txtframe.setText("0")
        self.ui.lblFPS.setText("%s" % info.get("fps"))

    def play(self):
        media_name = self.ui.cbMedia.currentText()
        if self.is_pause:
            if self.controller.cmd_to_media(media_name, get_key_media_play()):
                self.is_pause = False
                self._set_play_icon()
        else:
            if self.controller.cmd_to_media(media_name, get_key_media_pause()):
                self.is_pause = True
                self._set_play_icon()

    def active_loop(self):
        media_name = self.ui.cbMedia.currentText()
        self.controller.cmd_to_media(media_name, get_key_media_loop())

    def _set_play_icon(self):
        if not self.is_pause:
            self.ui.btnplay.setIcon(self.pause_icon)
        else:
            self.ui.btnplay.setIcon(self.play_icon)

    def _set_record_icon(self):
        if not self.is_recorded:
            self.ui.recordButton.setIcon(self.record_icon)
        else:
            self.ui.recordButton.setIcon(self.save_record_icon)

    def get_file_path(self):
        item_cbmedia = self.ui.cbMedia.currentText()
        media_type = self.dct_media.get(item_cbmedia, None)
        if media_type != get_media_type_video_name():
            return None
        return self.ui.movieLineEdit.text()
