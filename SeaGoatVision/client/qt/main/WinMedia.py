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
from SeaGoatVision.client.qt.shared_info import SharedInfo
from PySide.QtGui import QIcon
from SeaGoatVision.commons import keys
from SeaGoatVision.client.qt import config
from PySide.QtGui import QFileDialog
import threading
import time

from PySide import QtCore
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class WinMedia(QtCore.QObject):
    def __init__(self, controller):
        super(WinMedia, self).__init__()
        self.ressource_icon_path = "SeaGoatVision/client/ressource/img/"
        self.ui = None
        self.controller = controller
        self.shared_info = SharedInfo()
        self.shared_info.connect("start_execution", self.set_info)

        self.is_recorded = False
        self.is_play = False
        self.record_icon = QIcon(self.ressource_icon_path + "RecordVideoAction.png")
        self.save_record_icon = QIcon(self.ressource_icon_path + "SaveServerImageAction.png")
        self.play_icon = QIcon("/usr/share/icons/gnome/24x24/actions/player_play.png")
        self.pause_icon = QIcon("/usr/share/icons/gnome/24x24/actions/player_pause.png")

        self.dct_media = None
        self.last_selected_media = config.default_media_selected

        self.last_value_frame = 0
        self.max_frame = 0

        self.shared_info.connect("start_execution", self._start_execution)

        # TODO optimize starting thread.
        self.thread_player = PlayerFile(controller, self._get_actual_no_frame,
                                        self.set_slider_value)
        self.thread_player.start()
        self.reload_ui()

    def stop(self):
        if self.thread_player:
            self.thread_player.close()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.ui.recordButton.clicked.connect(self.click_record_button)
        self.ui.cbMedia.currentIndexChanged.connect(self._change_media)
        self.ui.openDirButton.clicked.connect(self.open_directory)
        self.ui.openFileButton.clicked.connect(self.open_file)
        self.ui.btnplay.clicked.connect(self.play)
        self.ui.loopchb.clicked.connect(self.active_loop)
        self.ui.movieLineEdit.textChanged.connect(self._movie_changed)
        self.ui.slider_frame.valueChanged.connect(self._slider_value_change)
        self.ui.txtframe.returnPressed.connect(self._txt_frame_value_change)
        self.ui.spin_box_fps.valueChanged.connect(self._change_fps)

        self._set_record_icon()
        self._set_play_icon()
        self._update_media()

        self.select_media(self.last_selected_media)

    def _update_media(self):
        self.ui.cbMedia.currentIndexChanged.disconnect(self._change_media)
        self.dct_media = self.controller.get_media_list()
        for media in self.dct_media.keys():
            self.ui.cbMedia.addItem(media)
        self._change_media(after_update=True)
        self.ui.cbMedia.currentIndexChanged.connect(self._change_media)

    def _change_media(self, index=-1, after_update=False):
        media_name = self.ui.cbMedia.currentText()
        frame_webcam = self.ui.frame_webcam
        frame_webcam.setVisible(False)
        frame_video = self.ui.frame_video
        frame_video.setVisible(False)

        media_type = self.dct_media.get(media_name, None)
        if not media_type:
            self.shared_info.set("media", None)
            return
        if media_type == keys.get_media_type_video_name():
            frame_video.setVisible(True)
        elif media_type == keys.get_media_type_streaming_name():
            frame_webcam.setVisible(True)
            self.shared_info.set("path_media", None)
        self.shared_info.set("media", media_name)
        self.set_info()
        if not after_update:
            self.last_selected_media = media_name

    def _movie_changed(self):
        self.shared_info.set("path_media", self.ui.movieLineEdit.text())

    def set_slider_value(self, value, force_value=False):
        last_value = self.ui.slider_frame.value()
        if last_value != value:
            self.ui.slider_frame.setValue(value)
        else:
            # force change value in video context
            self._slider_value_change(value)

    def _slider_value_change(self, value):
        self.ui.txtframe.setText(str(value))
        self._txt_frame_value_change()

    def _txt_frame_value_change(self):
        str_value = self.ui.txtframe.text()
        try:
            value = int(str_value)
        except:
            self.ui.txtframe.setText(str(self.last_value_frame))
            return
        if value < 1 or value > self.max_frame:
            self.ui.txtframe.setText(str(self.last_value_frame))
            return
        self.last_value_frame = value
        self.ui.txtframe.setText(str(value))
        self.set_frame_video(value)

    def _change_fps(self, value):
        self.thread_player.set_fps(value)

    def _get_actual_no_frame(self):
        return self.ui.slider_frame.value()

    def _start_execution(self, value=None):
        if not value or not isinstance(value, dict):
            return
        media_name = value.get("media")
        if media_name == keys.get_media_file_video_name():
            self.set_slider_value(1)
            self.is_play = False
            self.play()

    def click_record_button(self):
        if not self.is_recorded:
            path = self.ui.txt_name_record.text()
            if not path:
                path = None
            if self.ui.rbn_avi.isChecked():
                format_rec = keys.get_key_format_avi()
            else:
                format_rec = keys.get_key_format_png()
            options = {"compress": self.ui.sb_compress.value(), "format": format_rec}
            if not self.controller.start_record(self.ui.cbMedia.currentText(), path, options):
                # TODO improve error message
                logger.error("Trying start record...")
            else:
                self.is_recorded = True
        else:
            if not self.controller.stop_record(self.ui.cbMedia.currentText()):
                logger.error("Trying stop record...")
            self.is_recorded = False
        self.set_info()

    def open_directory(self):
        filename = QFileDialog.getExistingDirectory()
        if len(filename) > 0:
            self.ui.movieLineEdit.setText(filename)

    def open_file(self):
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) > 0:
            self.ui.movieLineEdit.setText(filename)

    def set_frame_video(self, value):
        media_name = self.shared_info.get("media")
        if not media_name:
            return
        self.controller.cmd_to_media(media_name, keys.get_key_media_frame(), value - 1)

    def set_info(self, value=None):
        # Ignore the value
        media_name = self.shared_info.get("media")
        if not media_name:
            return
        info = self.controller.get_info_media(media_name)
        if not info:
            logger.warning("WinMedia: info is empty from get_info_media.")
        self.max_frame = info.get("nb_frame", -1)
        self.ui.lblframe.setText("/%s" % self.max_frame)
        self.ui.txtframe.setText(str(self.last_value_frame))
        self.ui.slider_frame.setMinimum(1)
        self.ui.slider_frame.setMaximum(self.max_frame)
        self.thread_player.set_max_frame(self.max_frame)
        self.ui.lblFPS.setText("%s" % info.get("fps", "-1"))
        record_name = info.get("record_file_name", "")
        self.ui.txt_name_record.setText("%s" % record_name)
        self.is_recorded = bool(record_name)
        self._set_record_icon()

    def play(self):
        # media_name = self.ui.cbMedia.currentText()
        if self.is_play:
            # if self.controller.cmd_to_media(media_name,
            # keys.get_key_media_play()):
            self.thread_player.set_pause(True)
            self.is_play = False
            self._set_play_icon()
        else:
            # if self.controller.cmd_to_media(media_name,
            # keys.get_key_media_pause()):
            self.thread_player.set_pause(False)
            self.is_play = True
            self._set_play_icon()

    def active_loop(self):
        media_name = self.ui.cbMedia.currentText()
        self.controller.cmd_to_media(media_name, keys.get_key_media_loop(), None)

    def _set_play_icon(self):
        if not self.is_play:
            self.ui.btnplay.setIcon(self.play_icon)
        else:
            self.ui.btnplay.setIcon(self.pause_icon)

    def _set_record_icon(self):
        self.ui.sb_compress.setEnabled(not self.is_recorded)
        self.ui.rbn_avi.setEnabled(not self.is_recorded)
        self.ui.rbn_png.setEnabled(not self.is_recorded)
        self.ui.txt_name_record.setReadOnly(self.is_recorded)
        if not self.is_recorded:
            self.ui.recordButton.setIcon(self.record_icon)
        else:
            self.ui.recordButton.setIcon(self.save_record_icon)

    def get_file_path(self):
        item_cbmedia = self.ui.cbMedia.currentText()
        media_type = self.dct_media.get(item_cbmedia, None)
        if media_type != keys.get_media_type_video_name():
            return None
        return self.ui.movieLineEdit.text()

    def select_media(self, media_name):
        # find index
        index = self.ui.cbMedia.findText(media_name)
        if index < 0:
            return False
        # TODO Need to re-send signal if it's the same media? Maybe not
        # necessary
        self.ui.cbMedia.setCurrentIndex(index)
        return True


class PlayerFile(threading.Thread):
    def __init__(self, controller, call_get_frame, call_set_frame):
        threading.Thread.__init__(self)
        self.controller = controller
        self.call_get_frame = call_get_frame
        self.call_set_frame = call_set_frame
        self.set_fps(15)
        self.stop = False
        self.sleep_time = 1
        self.pause = True
        self.loop = True
        self.max_frame = 0
        self.fps = 0
        self.time_wait = 1

    def get_fps(self):
        return self.fps

    def set_max_frame(self, value):
        self.max_frame = value

    def set_fps(self, value):
        self.fps = value
        self.time_wait = 1.0 / value

    def set_pause(self, value):
        self.pause = value

    def run(self):
        # TODO optimize me if only 1 image
        # set first image
        while not self.stop:
            while self.pause:
                if self.stop:
                    return
                time.sleep(self.sleep_time)
            frame = self.call_get_frame()
            if self.max_frame <= frame:
                frame = 1
            else:
                frame += 1
            self.call_set_frame(frame)
            time.sleep(self.time_wait)

    def is_stopped(self):
        return self.stop

    def close(self):
        self.stop = True
