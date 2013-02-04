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

from CapraVision.client.qt.main.WinImageFolder import WinImageFolder
from CapraVision.client.qt.main.WinMovie import WinMovie
from CapraVision.client.qt.main.WinSingleImage import WinSingleImage

class WinSource:
    def __init__(self, source=None):
        self.source = source
        self.sourceUi = None

    def setSource(self, source):
        self.source = source
        self.sourceUi = self._getUi(source.__class__.__name__)

    def _getUi(self, sourceName):
        if sourceName == "ImageFolder":
            return WinImageFolder(self.source)
        elif sourceName == "Movie":
            return WinMovie(self.source)
        elif sourceName == "SingleImage":
            return WinSingleImage(self.source)
        else:
            return None

    def show(self):
        if self.sourceUi != None:
            self.sourceUi.show()