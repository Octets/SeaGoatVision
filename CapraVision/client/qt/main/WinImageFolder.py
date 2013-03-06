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
from PySide.QtGui import QFileDialog

class WinImageFolder:
    def __init__(self, imageFolder):
        self.ui = get_ui(self)
        self.imageFolder = imageFolder
        self.ui.openButton.clicked.connect(self.updateImageList)
        self.ui.autoPlayCheckBox.stateChanged.connect(self.autoPlay)
        self.ui.nextButton.clicked.connect(self.nextImage)
        self.ui.previousButton.clicked.connect(self.previousImage)
        self.ui.lastButton.clicked.connect(self.lastImage)
        self.ui.firstButton.clicked.connect(self.firstImage)

    def updateImageList(self):
        folderPath = QFileDialog.getExistingDirectory()
        if len(folderPath) > 0:
            self.imageFolder.read_folder(folderPath)
            self.imageFolder.load_image(0)

    def openNewFolder(self):
        pass

    def autoPlay(self, value):
        self.imageFolder.set_auto_increment(value)

    def nextImage(self):
        self.imageFolder.next()

    def firstImage(self):
        self.imageFolder.set_position(0)

    def previousImage(self):
        previousPos = self.imageFolder.current_position() - 1
        self.imageFolder.set_position(previousPos)

    def lastImage(self):
        lastPos = self.imageFolder.total_images() - 1
        self.imageFolder.set_position(lastPos)

    def show(self):
        self.ui.show()




