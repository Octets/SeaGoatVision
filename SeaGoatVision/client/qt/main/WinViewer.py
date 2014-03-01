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

"""
Description : Windows to "view" a filterchain execution
"""

import time

from SeaGoatVision.client.qt.utils import get_ui
from SeaGoatVision.commons import keys
from PIL import Image
from PySide import QtCore
from PySide import QtGui
from PySide.QtGui import QColor
from PySide.QtGui import QPen
# from PySide.QtCore import Qt
import socket
import threading
import StringIO
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class WinViewer(QtGui.QDockWidget):

    """Show the media after being processed by the filter chain.
    The window receives a filter in its constructor.
    This is the last executed filter on the media.
    """

    newImage = QtCore.Signal(QtGui.QImage)
    closePreview = QtCore.Signal(object)

    def __init__(self, controller, subscriber,
                 execution_name, media_name, filterchain_name, host, uid):
        super(WinViewer, self).__init__()
        self.host = host
        self.port = 5030

        self.controller = controller
        self.subscriber = subscriber
        self.execution_name = execution_name
        self.uid = uid
        self.filterchain_name = filterchain_name
        self.media_name = media_name
        self.is_turn_off = False
        self.execution_stopped = False

        self.ui = None
        self.actual_filter = None
        self.size = 1
        self.thread_output = None
        self.last_output = ""
        self.last_second_fps = None
        self.fps_count = 0

        self.reload_ui()

        self.light_observer = self._get_light_observer()

        if self.controller.add_image_observer(self.update_image, execution_name,
                                              self.actual_filter):
            self.__add_output_observer()
            self.subscriber.subscribe(self.media_name, self.update_fps)
            self.subscriber.subscribe(
                keys.get_key_execution_list(),
                self.update_execution)
        self.light_observer.start()

    def reload_ui(self):
        self.ui = get_ui(self)
        self.ui.lbl_media_name.setText(self.media_name)
        self.newImage.connect(self.set_pixmap)
        self.ui.filterComboBox.currentIndexChanged.connect(self._change_filter)
        self.ui.closeButton.clicked.connect(self.__close)
        self.ui.sizeComboBox.currentIndexChanged[
            str].connect(self.set_image_scale)

        self._update_filters()
        self.actual_filter = self.ui.filterComboBox.currentText()
        self.ui.lbl_exec.setText(self.execution_name)

    def closeEvent(self):
        # this is fake closeEvent, it's called by button close with signal
        if self.is_turn_off:
            return
        if not self.execution_stopped and self.actual_filter:
            self.controller.remove_image_observer(
                self.update_image,
                self.execution_name,
                self.actual_filter)
            self.controller.remove_output_observer(self.execution_name)
        if self.thread_output:
            self.thread_output.stop()
        self.subscriber.desubscribe(self.media_name, self.update_fps)
        self.light_observer.stop()
        logger.info("WinViewer %s quit." % (self.execution_name))

    #
    # PRIVATE FUNCTION  ############################
    #
    def _get_light_observer(self):
        # call me just one time
        light_widget = LightWidget()
        size = self.ui.qhboxlayout_2.minimumSize()
        min_size = min(size.width(), size.height())
        light_widget.setGeometry(0, 0, min_size, min_size)

        self.ui.qhboxlayout_2.addWidget(light_widget)
        return LightObserver(light_widget)

    def __close(self):
        self.closePreview.emit(self.uid)

    def __add_output_observer(self):
        self.thread_output = ListenOutput(
            self.update_log,
            self.host,
            self.port)
        self.thread_output.start()
        # TODO fait un thread de client dude
        self.controller.add_output_observer(self.execution_name)

    def _update_filters(self):
        self.ui.filterComboBox.clear()
        info = self.controller.get_filterchain_info(self.filterchain_name)
        if not info:
            logger.error("Missing info from get_filterchain_info.")
            return
        lst_filter = info.get("filters", None)
        if not lst_filter:
            logger.warning(
                "Recieve empty filter list from filterchain %s" %
                self.filterchain_name)
            return
        for sFilter in lst_filter:
            self.ui.filterComboBox.addItem(sFilter.get("name", ""))
        self.ui.filterComboBox.setCurrentIndex(
            self.ui.filterComboBox.count() - 1)

    def _change_filter(self):
        if self.actual_filter:
            filter_name = self.ui.filterComboBox.currentText()
            self.controller.set_image_observer(
                self.update_image,
                self.execution_name,
                self.actual_filter,
                filter_name)
            self.actual_filter = filter_name

    def update_log(self, data):
        data = str(data).strip()
        logger.info("Qt output exec %s - %s" % (self.execution_name, data))

    def update_fps(self, data):
        self.ui.lbl_fps.setText("%s" % data)

    def update_image(self, image):
        self.light_observer.active_light()
        # fps
        actual_time = time.time()
        if self.last_second_fps is None:
            # Initiate fps
            self.last_second_fps = actual_time
            self.fps_count = 1
        elif actual_time - self.last_second_fps > 1.0:
            self.ui.lbl_stream_fps.setText("%d" % int(self.fps_count))
            # new set
            self.last_second_fps = actual_time
            self.fps_count = 1
        else:
            self.fps_count += 1

        try:
            self.numpy_to_qimage(image)
        except Exception as e:
            log.printerror_stacktrace(logger, e, check_duplicate=True)

    def set_pixmap(self, img):
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.imageLabel.setPixmap(pix)

    def numpy_to_qimage(self, image):
        img = Image.fromarray(image)
        buff = StringIO.StringIO()
        img.save(buff, 'ppm')
        data = buff.getvalue()
        buff.close()
        qimage = QtGui.QImage.fromData(data)
        if self.size != 1.0:
            shape = image.shape
            qimage = qimage.scaled(shape[1] * self.size, shape[0] * self.size)
        self.newImage.emit(qimage)

    def set_image_scale(self, text_size):
        text_size = text_size[:-1]
        self.size = float(text_size) / 100

    def update_execution(self, data):
        # check if the execution name is removed
        operator = data[0]
        execution_name = data[1:]
        if operator == "-" and execution_name == self.execution_name:
            self.execution_stopped = True
            self.light_observer.turn_off()
            self.closeEvent()
            self.is_turn_off = True


class ListenOutput(threading.Thread):

    def __init__(self, observer, host, port):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_stopped = False
        self.observer = observer
        self.host = host
        self.port = port
        self.count_empty_message = 0

    def run(self):
        self.socket.connect((self.host, self.port))
        try:
            while not self.is_stopped:
                txt = self.socket.recv(2048)
                if not txt:
                    self.count_empty_message += 1
                    if self.count_empty_message > 6:
                        self.is_stopped = True
                        break
                    continue

                self.observer(txt)
        except:
            self.is_stopped = True

    def stop(self):
        self.is_stopped = True
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()


class LightObserver(threading.Thread):

    def __init__(self, uiwidget):
        threading.Thread.__init__(self)
        self.uiwidget = uiwidget
        self.light = False
        self.is_stopped = False

    def active_light(self):
        self.light = True

    def turn_off(self):
        self.stop()
        self.uiwidget.set_black()

    def run(self):
        while not self.is_stopped:
            if self.light:
                self.uiwidget.set_green()
                self.light = False
            else:
                self.uiwidget.set_red()
            time.sleep(1)

    def stop(self):
        self.is_stopped = True


class LightWidget(QtGui.QWidget):

    def __init__(self):
        super(LightWidget, self).__init__()
        self.color = QColor()
        self.last_is_red = True
        self.set_red()
        self.is_black = False

    def set_red(self):
        self.color.setRgb(255, 0, 0)
        if not self.last_is_red:
            try:
                self.update()
            except Exception:
                pass
        self.last_is_red = True

    def set_green(self):
        self.color.setRgb(0, 255, 0)
        if self.last_is_red:
            try:
                self.update()
            except Exception:
                pass
        self.last_is_red = False

    def set_black(self):
        self.color.setRgb(0, 0, 0)
        try:
            self.update()
        except Exception:
            pass
        self.is_black = True

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_widget(qp)
        qp.end()

    def draw_widget(self, qp):
        size = self.size()
        radx = size.width()
        rady = size.height()
        dot = min(radx, rady) / 2

        pen = QPen()
        pen.setWidth(dot)
        # pen.setStyle(Qt.SolidLine)
        pen.setBrush(self.color)
        # pen.setCapStyle(Qt.RoundCap)
        # pen.setJoinStyle(Qt.RoundJoin)
        qp.setPen(pen)

        qp.drawLine(dot, dot, dot, dot)
