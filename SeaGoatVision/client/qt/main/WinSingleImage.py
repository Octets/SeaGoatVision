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

from PySide.QtGui import QFileDialog

class WinSingleImage:
    def __init__(self, simpleImage):
        self.simpleImage = simpleImage

    def show(self):
        filename = QFileDialog.getOpenFileName(filter="Images(*.png *.jpg *.xpm)")[0]
        if len(filename) > 0:
            self.setImage(filename)

    def setImage(self, filename):
        self.simpleImage.set_image(filename)