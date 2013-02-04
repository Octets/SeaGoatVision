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

from CapraVision.client.qt.utils import get_ui
from CapraVision.server.imageproviders import supported_video_formats
from PySide.QtGui import QFileDialog

class WinMovie:
    def __init__(self, movie):
        self.ui = get_ui(self)
        self.movie = movie
        self.ui.openButton.clicked.connect(self.openNewMovie)
        self.ui.playButton.clicked.connect(self.play)
        self.ui.pauseButton.clicked.connect(self.pause)

    def openNewMovie(self):
        filename = QFileDialog.getOpenFileName(filter="Movie(" + self._getVideoFormat() + ")")[0]
        if len(filename) > 0:
            self.movie.open_video_file(filename)

    def _getVideoFormat(self):
        rawFormats = supported_video_formats()
        formats = " *".join(rawFormats)
        return "*" + formats


    def play(self):
        self.movie.play()

    def pause(self):
        self.movie.pause()

    def track(self):
        pass

    def show(self):
        self.ui.show()


