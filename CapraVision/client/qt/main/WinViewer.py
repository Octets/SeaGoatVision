#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of CapraVision.
#
#    CapraVision is free software: you can redistribute it and/or modify
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

# from gi.repository import GObject

"""
Description : Windows to "view" a filterchain execution
Authors: Mathieu Benoit (mathben963@gmail.com)
         Junior Gregoire (junior.gregoire@gmail.com)
Date : december 2012
"""

import time

from CapraVision.client.qt.utils import get_ui
from CapraVision.server.filters.implementation.bgr2rgb import BGR2RGB
import Image
from PySide import QtCore
from PySide import QtGui
import socket
import threading
import StringIO

class WinViewer(QtCore.QObject):
    """Show the source after being processed by the filter chain.
    The window receives a filter in its constructor.
    This is the last executed filter on the source.
    """

    newImage = QtCore.Signal(QtGui.QImage)
    closePreview = QtCore.Signal(object)

    def __init__(self, controller, execution_name, source_name, filterchain_name, lst_filter_str):
        super(WinViewer, self).__init__()
        self.ui = get_ui(self, 'sourcesListStore', 'filterChainListStore')

        self.controller = controller
        self.execution_name = execution_name
        self.filterchain_name = filterchain_name

        self.actualFilter = None
        self.size = 1
        self.thread_output = None
        self.last_output = ""
        self.lastSecondFps = None
        self.fpsCount = 0

        self.newImage.connect(self.setPixmap)
        self.ui.filterComboBox.currentIndexChanged.connect(self._changeFilter)
        self.ui.closeButton.clicked.connect(self.__close)
        self.ui.sizeComboBox.currentIndexChanged[str].connect(self.setImageScale)

        self._updateFilters(lst_filter_str)
        self.controller.start_filterchain_execution(execution_name, source_name, filterchain_name)
        self.actualFilter = self.ui.filterComboBox.currentText()

        self.controller.add_image_observer(self.updateImage, execution_name, self.actualFilter)
        self.__add_output_observer()

    def closeEvent(self):
        # this is fake closeEvent, it's called by button close with signal
        if self.actualFilter:
            self.controller.remove_image_observer(self.updateImage, self.execution_name, self.actualFilter)
            self.controller.remove_output_observer(self.execution_name)
            self.controller.stop_filterchain_execution(self.execution_name)
        if self.thread_output:
            self.thread_output.stop()
        print("WinViewer %s quit." % (self.execution_name))

    ######################################################################
    ####################### PRIVATE FUNCTION  ############################
    ######################################################################
    def __close(self):
        self.closePreview.emit(self.execution_name)

    def __add_output_observer(self):
        self.thread_output = Listen_output(self.updateLog)
        self.thread_output.start()
        ########### TODO fait un thread de client dude
        self.controller.add_output_observer(self.execution_name)

    def _updateFilters(self, lst_filter_str):
        self.ui.filterComboBox.clear()
        for sFilter in lst_filter_str:
            self.ui.filterComboBox.addItem(sFilter)

    def _changeFilter(self):
        if self.actualFilter:
            filter_name = self.ui.filterComboBox.currentText()
            self.controller.set_image_observer(self.updateImage, self.execution_name, self.actualFilter, filter_name)
            self.actualFilter = filter_name

    def updateLog(self, data):
        data = str(data).strip()
        print data
        if data and self.last_output != data:
            self.last_output = data
            self.ui.txtLog.insertPlainText(data + "\n")

    def updateImage(self, image):
        # fps
        iActualTime = time.time()
        if self.lastSecondFps is None:
            # Initiate fps
            self.lastSecondFps = iActualTime
            self.fpsCount = 1
        elif iActualTime - self.lastSecondFps > 1.0:
            self.ui.lbl_fps.setText("%d" % int(self.fpsCount))
            # new set
            self.lastSecondFps = iActualTime
            self.fpsCount = 1
        else:
            self.fpsCount += 1

        self.numpy_to_QImage(image)

    def setPixmap(self, img):
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.imageLabel.setPixmap(pix)

    def numpy_to_QImage(self, image):
        bgr2rgb = BGR2RGB()
        imageRGB = bgr2rgb.execute(image)
        img = Image.fromarray(imageRGB)
        buff = StringIO.StringIO()
        img.save(buff, 'ppm')
        data = buff.getvalue()
        buff.close()
        qimage = QtGui.QImage.fromData(data)
        if self.size <> 1.0:
            shape = image.shape
            qimage = qimage.scaled(shape[1] * self.size, shape[0] * self.size)
        self.newImage.emit(qimage)

    def setImageScale(self, textSize):
        textSize = textSize[:-1]
        self.size = float(textSize) / 100

class Listen_output(threading.Thread):
    def __init__(self, observer):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_stopped = False
        self.observer = observer

    def run(self):
        self.socket.connect(("127.0.0.1", 5030))
        while not self.is_stopped:
            self.observer(self.socket.recv(2048))

    def stop(self):
        self.is_stopped = True
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()

